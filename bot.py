import asyncio
import logging
from aiogram import Bot, Dispatcher
from Config_data.config import Config, load_config
from Handlers import other_handlers, admin_handlers
from aiogram_dialog import setup_dialogs
import aioschedule
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from time_messange import send_message
from datetime import datetime


# Инициализируем логер
logger = logging.getLogger(__name__)


# Функция конфигурировани и запуска бота
async def main() -> None:
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )

    # Выводим в консоль информацию о начале запуска
    logger.info('Starting Lesson')

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инциализируем бота и диспетчера
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher()

    # Сообщения по расписанию
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(send_message, trigger='cron', hour=7, minute=42, start_date=datetime.now(), kwargs={'bot': bot})
    scheduler.start()

    # Регистрируем роутеры
    dp.include_router(admin_handlers.router)
    dp.include_router(other_handlers.router)
    dp.include_router(admin_handlers.start_dialog)
    setup_dialogs(dp)

    # Пропускать накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())