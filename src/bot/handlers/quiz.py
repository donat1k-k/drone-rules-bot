from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.keyboards import back_kb

router = Router()


class QuizState(StatesGroup):
    answering = State()


_QUESTIONS = [
    {
        "text": "На каком заряде аккумулятора рекомендуется возвращать дрон домой?",
        "options": ["5–10%", "20–30%", "50%", "60%"],
        "correct": 1,
        "explanation": "20–30% — достаточно времени для безопасной посадки без риска потери дрона.",
    },
    {
        "text": "В России государственному учёту подлежат БВС с максимальной взлётной массой:",
        "options": ["Любой массы", "От 150 г до 30 кг", "Более 500 г", "Более 1 кг"],
        "correct": 1,
        "explanation": "От 150 г до 30 кг — госучёт обязателен. ⚠️ Уточняй актуальные нормы на favt.gov.ru.",
    },
    {
        "text": "Где проверить запрещённые зоны перед полётом?",
        "options": ["В боте", "В соцсетях", "На сайте Росавиации / в Небосводе", "Не нужно"],
        "correct": 2,
        "explanation": "Всегда проверяй на favt.gov.ru или в официальном сервисе Небосвод перед каждым вылетом.",
    },
    {
        "text": "Что делает большинство современных дронов при потере сигнала?",
        "options": ["Зависает на месте", "Падает вниз", "Летит к точке взлёта (RTH)", "Ускоряется вперёд"],
        "correct": 2,
        "explanation": "RTH (Return to Home) — автовозврат. Настрой его высоту выше препятствий заранее.",
    },
    {
        "text": "При каком ветре полёт не рекомендуется?",
        "options": ["3–4 м/с", "5–7 м/с", "Более 8–10 м/с", "Ветер не влияет"],
        "correct": 2,
        "explanation": "При ветре выше 8–10 м/с управление нестабильно. Проверяй прогноз перед вылетом.",
    },
]

_TOTAL = len(_QUESTIONS)


def _question_kb(q_idx: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for i, opt in enumerate(_QUESTIONS[q_idx]["options"]):
        builder.button(text=opt, callback_data=f"quiz_ans:{i}")
    builder.adjust(2)
    return builder.as_markup()


def _format_question(idx: int) -> str:
    q = _QUESTIONS[idx]
    opts = "\n".join(f"{i + 1}. {opt}" for i, opt in enumerate(q["options"]))
    return f"*Вопрос {idx + 1}/{_TOTAL}:*\n{q['text']}\n\n{opts}"


@router.callback_query(lambda c: c.data == "quiz")
async def cb_quiz_start(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(QuizState.answering)
    await state.update_data(q_idx=0, score=0)
    text = (
        "🧠 *Мини-тест: правила полётов*\n\n"
        "5 вопросов по безопасности, регистрации и нештатным ситуациям.\n\n"
        + _format_question(0)
    )
    await callback.message.edit_text(text, reply_markup=_question_kb(0), parse_mode="Markdown")
    await callback.answer()


@router.callback_query(
    lambda c: c.data and c.data.startswith("quiz_ans:"),
    StateFilter(QuizState.answering),
)
async def cb_quiz_answer(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    q_idx: int = data["q_idx"]
    score: int = data["score"]
    ans_idx = int(callback.data.split(":")[1])

    q = _QUESTIONS[q_idx]
    is_correct = ans_idx == q["correct"]
    if is_correct:
        score += 1
        feedback = f"✅ *Верно!*\n_{q['explanation']}_"
    else:
        feedback = (
            f"❌ *Неверно.* Правильный ответ: «{q['options'][q['correct']]}».\n"
            f"_{q['explanation']}_"
        )

    q_idx += 1
    await state.update_data(q_idx=q_idx, score=score)

    if q_idx < _TOTAL:
        text = feedback + "\n\n" + _format_question(q_idx)
        await callback.message.edit_text(text, reply_markup=_question_kb(q_idx), parse_mode="Markdown")
    else:
        await state.clear()
        if score == _TOTAL:
            grade = "🎉 Отлично — все правильно!"
        elif score >= 3:
            grade = "👍 Хороший результат!"
        else:
            grade = "📚 Стоит повторить правила."
        text = feedback + f"\n\n🏁 *Тест завершён! Результат: {score}/{_TOTAL}*\n{grade}"
        await callback.message.edit_text(text, reply_markup=back_kb(), parse_mode="Markdown")

    await callback.answer("✅" if is_correct else "❌")
