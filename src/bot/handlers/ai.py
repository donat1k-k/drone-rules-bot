from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from src.ai import client as ai_client
from src.bot.keyboards import back_kb

router = Router()


class AiState(StatesGroup):
    waiting_question = State()


_INTRO = (
    "🤖 *AI-режим*\n\n"
    "Напиши свой вопрос о дронах — постараюсь ответить.\n\n"
    "⚠️ _AI может ошибаться. Юридические вопросы всегда проверяй "
    "на официальных источниках._"
)


@router.callback_query(lambda c: c.data == "ai")
async def cb_ai(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AiState.waiting_question)
    await callback.message.edit_text(
        _INTRO, reply_markup=back_kb(), parse_mode="Markdown"
    )
    await callback.answer()


@router.message(StateFilter(AiState.waiting_question))
async def handle_ai_question(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    answer = await ai_client.ask(message.text or "")
    await message.answer(answer, reply_markup=back_kb())
