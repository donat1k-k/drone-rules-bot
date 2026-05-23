from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from src.bot.keyboards import back_kb
from src.weather import client as weather_client

router = Router()


class WeatherState(StatesGroup):
    waiting_location = State()


_INTRO = (
    "🌦 *Погода для полёта*\n\n"
    "Введи название города или координаты в формате `55.75, 37.61`.\n\n"
    "_Примеры: Москва, Краснодар, -33.86, 151.21_"
)

_DISCLAIMER = (
    "\n\n⚠️ _Это справочная погодная оценка. Она не является разрешением на полёт "
    "и не заменяет проверку запретных зон, правил и здравого смысла._"
)


@router.callback_query(lambda c: c.data == "weather")
async def cb_weather(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(WeatherState.waiting_location)
    await callback.message.edit_text(_INTRO, reply_markup=back_kb(), parse_mode="Markdown")
    await callback.answer()


@router.message(StateFilter(WeatherState.waiting_location))
async def handle_weather_location(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")

    result = await weather_client.get_weather_for_location(message.text or "")

    if result.get("error") == "not_found":
        await message.answer(
            "🔍 Город не найден. Попробуй ввести координаты в формате `55.75, 37.61`.",
            reply_markup=back_kb(),
            parse_mode="Markdown",
        )
        return

    if result.get("error") == "api_unavailable":
        await message.answer(
            "⚠️ Сервис погоды временно недоступен. Попробуй позже.",
            reply_markup=back_kb(),
        )
        return

    a = result["assessment"]
    text = (
        f"🌍 *{result['location']}*\n\n"
        f"🌡 Температура: {result['temp']:.1f}°C\n"
        f"💨 Ветер: {result['wind']:.1f} м/с\n"
        f"🌧 Осадки: {result['precip']:.1f} мм\n\n"
        f"{a['emoji']} *{a['text'].capitalize()}*"
        f"{_DISCLAIMER}"
    )
    await message.answer(text, reply_markup=back_kb(), parse_mode="Markdown")
