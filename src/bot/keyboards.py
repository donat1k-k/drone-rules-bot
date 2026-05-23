from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

_SECTIONS = [
    ("🚁 Подготовка к полёту", "topic:preparation"),
    ("🛡 Правила безопасности", "topic:safety"),
    ("🚫 Запрещённые зоны", "topic:restricted_zones"),
    ("📋 Регистрация и закон", "topic:registration"),
    ("📶 Потеря сигнала", "topic:signal_loss"),
    ("💡 Советы новичкам", "topic:tips"),
    ("❓ FAQ", "topic:faq"),
    ("🔗 Полезные ссылки", "topic:links"),
]


def main_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for label, cb_data in _SECTIONS:
        builder.button(text=label, callback_data=cb_data)
    builder.adjust(1)
    return builder.as_markup()


def back_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="← Главное меню", callback_data="menu")
    return builder.as_markup()
