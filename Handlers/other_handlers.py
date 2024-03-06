from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from Keyboards.keyboaeds import create_key, create_inline_key
from Lexicon.lexicon_ru import LEXICON_MENU, LEXICON_INLINE
from Config_BD.users_bd import SQL


router: Router = Router()
keyboard_start = create_key(2, **LEXICON_MENU)
keyboard_inline = create_inline_key(2, 'Site', **LEXICON_INLINE)


# Создаем базу данных пользователей
user_dict: dict[int, dict[str, str | int | bool]] = {}


class FSMFillForm(StatesGroup):
    fill_name = State()
    fill_age = State()
    fill_phone = State()


@router.message(CommandStart())
async def process_start_comand(message: Message):
    s = SQL()
    s.INSERT(message.from_user.id, message.from_user.first_name, message.from_user.username)
    await message.answer('HI', reply_markup=keyboard_start)


@router.message(F.text == 'HI BOT')
async def hi(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, 'HI USER')


@router.message(F.text == '/my_id')
async def hi(message: Message):
    await message.answer(str(message.from_user.id))


@router.message(F.text == 'Заполнить Анкету')
async def anceta_start(message: Message, state: FSMContext):
    await message.answer('Давайте заполним Анкету')
    await message.answer('Пожалуйста введите Ваше имя')
    # устанавливаем состояние ожидания ввода имени
    await state.set_state(FSMFillForm.fill_name)


@router.message(StateFilter(FSMFillForm.fill_name), F.text.isalpha())
async def anceta_name(message: Message, state: FSMContext):
    # Сохраняем введенное имя в хранилище
    await state.update_data(name=message.text)
    await message.answer('Спасибо, Теперь введите Ваш Возраст')
    # устанавливаем состояние ожидания ввода возраста
    await state.set_state(FSMFillForm.fill_age)


@router.message(StateFilter(FSMFillForm.fill_name))
async def anceta_name(message: Message, state: FSMContext):
    await message.answer('Некорректный ввод имени, Теперь введите Ваше имя буквами')
    # устанавливаем состояние ожидания ввода возраста
    await state.set_state(FSMFillForm.fill_name)


@router.message(StateFilter(FSMFillForm.fill_age))
async def anceta_name(message: Message, state: FSMContext):
    # Сохраняем введенный возраст в хранилище
    await state.update_data(age=message.text)
    await message.answer('Спасибо, Теперь введите Ваш Телефон')
    # устанавливаем состояние ожидания ввода телефона
    await state.set_state(FSMFillForm.fill_phone)


@router.message(StateFilter(FSMFillForm.fill_phone))
async def anceta_name(message: Message, state: FSMContext):
    # Сохраняем введенный телефон в хранилище
    await state.update_data(phone=message.text)
    user_dict[message.from_user.id] = await state.get_data()
    await state.clear()
    await message.answer('Спасибо, Ваши данные с охранены')
    # Отправляем пользователю сохраненные данные
    if message.from_user.id in user_dict:
        await message.answer(text=f'Имя: {user_dict[message.from_user.id]["name"]} \n'
                                  f'Возраст: {user_dict[message.from_user.id]["age"]} \n'
                                  f'Телефон: {user_dict[message.from_user.id]["phone"]} \n'
                             )
    else:
        await message.answer('Вы еще не заполняли анкету', reply_markup=keyboard_start)


@router.message(F.text == 'Сказать привет')
async def anceta_start(message: Message):
    await message.answer('Привет', reply_markup=keyboard_inline)


@router.callback_query(F.text == '1')
async def anceta_start(callback: CallbackQuery):
    try:
        await callback.message.edit_text('Нажали первую кнопку', reply_markup=keyboard_inline)
    except:
        await callback.answer('Уже Нажали первую кнопку')


@router.callback_query(F.text == '2')
async def anceta_start(callback: CallbackQuery):
    await callback.answer('Нажали вторую кнопку')
    await callback.message.edit_text('Нажали вторую кнопку', reply_markup=keyboard_inline)

