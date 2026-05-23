from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from src.bot.keyboards import main_menu_kb, search_result_kb
from src.knowledge.search import search_knowledge

router = Router()

_WELCOME = (
    "👋 Привет! Я бот-инструктор по правилам управления дронами.\n\n"
    "Выбери раздел из меню ниже.\n\n"
    "⚠️ *Дисклеймер:* вся информация носит *справочный* характер — "
    "это не юридическая консультация. Перед полётом сверяйся "
    "с официальными источниками и актуальным законодательством."
)

_HELP = (
    "🛸 *Бот «Правила управления дронами»*\n\n"
    "Используй кнопки меню для навигации по разделам.\n"
    "Можешь написать вопрос текстом — я попробую найти ответ в базе знаний.\n\n"
    "Доступные разделы:\n"
    "🚁 Подготовка к полёту\n"
    "🛡 Правила безопасности\n"
    "🚫 Запрещённые зоны\n"
    "📋 Регистрация и закон\n"
    "📶 Потеря сигнала\n"
    "💡 Советы новичкам\n"
    "❓ FAQ\n"
    "🔗 Полезные ссылки\n\n"
    "⚠️ Информация справочная — всегда проверяй на официальных ресурсах."
)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(_WELCOME, reply_markup=main_menu_kb(), parse_mode="Markdown")


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(_HELP, reply_markup=main_menu_kb(), parse_mode="Markdown")


@router.callback_query(lambda c: c.data == "menu")
async def cb_menu(callback: CallbackQuery) -> None:
    try:
        await callback.message.edit_text(
            _WELCOME, reply_markup=main_menu_kb(), parse_mode="Markdown"
        )
    except TelegramBadRequest:
        pass
    await callback.answer()


@router.message()
async def fallback(message: Message) -> None:
    result = search_knowledge(message.text or "")
    if result:
        text = (
            f"🔍 Похоже, ответ в разделе:\n"
            f"*{result['title']}*\n\n"
            "Открой раздел для подробностей 👇"
        )
        await message.answer(
            text, reply_markup=search_result_kb(result["id"]), parse_mode="Markdown"
        )
    else:
        await message.answer(
            "Не нашёл ответа на твой вопрос 🤔\n"
            "Попробуй открыть нужный раздел из меню 👇",
            reply_markup=main_menu_kb(),
        )
