from aiogram.types import KeyboardButton, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from Lexicon.lexicon_ru import LEXICON_INLINE


def create_key(width: int, *args: str, **kwargs: str):
    # Инициализация билдера для клавиатуры
    menu: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

    # Инициализируем список кнопок
    buttons: list[KeyboardButton] = []

    if args:
        for button in args:
            buttons.append(KeyboardButton(text=button))

    if kwargs:
        for key, val in kwargs.items():
            buttons.append(KeyboardButton(text=val))

    menu.row(*buttons, width=width)
    return menu.as_markup()


def create_inline_key(width: int, button1: str | None = None, *args: str, **kwargs: str):
    # Инициализация билдера для клавиатуры
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    # Инициализируем список кнопок
    buttons: list[InlineKeyboardButton] = []

    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(text=LEXICON_INLINE[button] if button in LEXICON_INLINE else button, callback_data=button))

    if kwargs:
        for key, button in kwargs.items():
            buttons.append(InlineKeyboardButton(text=button, callback_data=key))

    kb_builder.row(*buttons, width=width)
    if button1:
        kb = InlineKeyboardButton(text=button1, web_app=WebAppInfo(url='https://dzen.ru/a/ZQf-tVJqRiYlaJ_S?referrer_clid=1400&'))
        kb_builder.row(kb)
    return kb_builder.as_markup()