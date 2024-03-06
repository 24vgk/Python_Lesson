from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Group
from aiogram.fsm.state import default_state, State, StatesGroup
from Filters.filters import IsAdmin
from Keyboards.keyboaeds import create_key, create_inline_key
from Lexicon.lexicon_ru import LEXICON_MENU_ADMIN, LEXICON_INLINE
from Config_BD.users_bd import SQL


router: Router = Router()
router.message.filter(IsAdmin())
keyboard_start = create_key(2, **LEXICON_MENU_ADMIN)


class StartD(StatesGroup):
    start = State()
    update = State()


@router.message(CommandStart())
async def process_start_admin(message: Message):
    s = SQL()
    s.INSERT(message.from_user.id, message.from_user.first_name, message.from_user.username)
    await message.answer('ПРИВЕТ АДМИН!!!', reply_markup=keyboard_start)


@router.message(F.text == 'В ДИАДЛОГ')
async def dialog_start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartD.start, mode=StartMode.RESET_STACK)


async def update_name(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    s = SQL()
    s.UPDATE('NEW_NAME', callback.from_user.id)
    result = s.SELECT('NEW_NAME')
    s.DELETE('NEW_NAME')
    await callback.message.answer(str(result[1]))
    await dialog_manager.switch_to(state=StartD.update)


start_dialog = Dialog(
    Window(
        Const('Ты вошел в Диалог'),
        Group(
            Button(Const('Изменить ИМЯ'), id='name', on_click=update_name),
            width=1
        ),
        state=StartD.start
    ),
    Window(
        Const('Ты поменял имя!'),
        state=StartD.update
    )
)