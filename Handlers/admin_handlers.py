from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.text import Const
from Filters.filters import IsAdmin
from Keyboards.keyboaeds import create_key, create_inline_key
from Lexicon.lexicon_ru import LEXICON_MENU_ADMIN, LEXICON_INLINE
from Config_BD.users_bd import SQL


router: Router = Router()
router.message.filter(IsAdmin())
keyboard_start = create_key(2, **LEXICON_MENU_ADMIN)


class StartD(StatesGroup):
    start = State()


@router.message(CommandStart())
async def process_start_comand(message: Message):
    await message.answer('ТЫ АДМИНИСТРАТОР', reply_markup=keyboard_start)



@router.message()
async def process_start_comand(message: Message, dialog_manager: DialogManager):
    await message.answer('ПРИВЕТ АДМИНИСТРАТОР', reply_markup=keyboard_start)
    await dialog_manager.start(state=StartD.start, mode=StartMode.RESET_STACK)


start_dialog = Dialog(
    Window(
        Const('Привет Админ ты в Диалоге!'),
        state=StartD.start
    )
)