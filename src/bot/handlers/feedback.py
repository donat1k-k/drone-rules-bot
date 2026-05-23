from datetime import datetime
from pathlib import Path

from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from src.bot.keyboards import back_kb, main_menu_kb

router = Router()

_FEEDBACK_FILE = Path("logs/feedback.txt")


class FeedbackState(StatesGroup):
    waiting_question = State()


def _save(text: str) -> None:
    _FEEDBACK_FILE.parent.mkdir(exist_ok=True)
    with _FEEDBACK_FILE.open("a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat(timespec='seconds')}] {text}\n")


@router.callback_query(lambda c: c.data == "feedback_ask")
async def cb_feedback_ask(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(FeedbackState.waiting_question)
    await callback.message.edit_text(
        "✍️ Напиши свой вопрос — я сохраню его.\n\n"
        "Постараемся добавить ответ в базу знаний.\n"
        "Личные данные не сохраняются.",
        reply_markup=back_kb(),
    )
    await callback.answer()


@router.message(StateFilter(FeedbackState.waiting_question))
async def handle_feedback(message: Message, state: FSMContext) -> None:
    await state.clear()
    _save(message.text or "(пустое сообщение)")
    await message.answer(
        "✅ Вопрос сохранён. Спасибо!\n\n"
        "Попробуй поиск или открой меню 👇",
        reply_markup=main_menu_kb(),
    )
