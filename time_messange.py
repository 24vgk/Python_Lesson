from aiogram import Bot
from Lexicon.lexicon_ru import LEXICON_TIME


async def send_message(bot: Bot):
    await bot.send_message(725455605, LEXICON_TIME['mes'])