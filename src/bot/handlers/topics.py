from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, LinkPreviewOptions

from src.bot.keyboards import back_kb
from src.knowledge.loader import load_topic

router = Router()

_PREVIEW_OFF = LinkPreviewOptions(is_disabled=True)


@router.callback_query(lambda c: c.data and c.data.startswith("topic:"))
async def cb_topic(callback: CallbackQuery) -> None:
    topic_id = callback.data.split(":", 1)[1]
    data = load_topic(topic_id)

    text = f"*{data['title']}*\n\n{data['body'].strip()}"
    if data.get("disclaimer"):
        text += f"\n\n⚠️ _{data['disclaimer']}_"

    try:
        await callback.message.edit_text(
            text,
            reply_markup=back_kb(),
            parse_mode="Markdown",
            link_preview_options=_PREVIEW_OFF,
        )
    except TelegramBadRequest:
        pass
    await callback.answer()
