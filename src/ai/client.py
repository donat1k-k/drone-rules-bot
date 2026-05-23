from __future__ import annotations

import logging
import re

from src import config
from src.knowledge.loader import load_topic

logger = logging.getLogger(__name__)

_TOPIC_IDS = [
    "preparation", "safety", "restricted_zones", "registration",
    "signal_loss", "tips", "faq", "links",
]

_SYSTEM_PROMPT_TEMPLATE = """\
Ты — ИИ-ассистент Telegram-бота «Правила управления дронами для начинающих».
Отвечай начинающим пилотам коротко, простым языком, без жаргона.

СТРОГИЕ ПРАВИЛА:
1. Отвечай ТОЛЬКО на вопросы по теме: дроны, подготовка к полёту, безопасность, \
запрещённые зоны, регистрация дронов, потеря сигнала, советы новичкам.
2. НЕ выдумывай конкретные номера законов, статей, суммы штрафов, точные весовые пороги.
3. По юридическим вопросам давай общий ответ и рекомендуй проверить на официальных \
ресурсах: Росавиация (favt.gov.ru), Госуслуги (gosuslugi.ru).
4. Если вопрос НЕ по теме дронов — вежливо откажись и предложи открыть меню бота.
5. ВСЕГДА завершай ответ строкой: «ℹ️ Информация справочная — сверяй с официальными источниками.»

ФОРМАТ ОТВЕТА — строго plain text:
- НЕ используй **жирный**, *курсив*, __подчёркивание__, ~~зачёркивание__.
- НЕ используй заголовки Markdown (### Заголовок).
- НЕ используй таблицы Markdown.
- Списки — только через "1.", "2.", "-" без какого-либо форматирования вокруг текста.
- Пиши обычный текст — он отправляется в Telegram как есть, без рендеринга Markdown.

БАЗА ЗНАНИЙ БОТА (разделы):
{knowledge}
"""

_knowledge_context: str | None = None


def _build_knowledge_context() -> str:
    parts = []
    for topic_id in _TOPIC_IDS:
        try:
            topic = load_topic(topic_id)
            kw = ", ".join(topic.get("keywords", [])[:8])
            parts.append(f"• {topic['title']} (темы: {kw})")
        except Exception:
            pass
    return "\n".join(parts)


def _system_prompt() -> str:
    global _knowledge_context
    if _knowledge_context is None:
        _knowledge_context = _build_knowledge_context()
    return _SYSTEM_PROMPT_TEMPLATE.format(knowledge=_knowledge_context)


def _strip_markdown(text: str) -> str:
    """Remove common Markdown symbols that render as raw text in Telegram plain mode."""
    text = re.sub(r'\*{1,3}', '', text)       # *, **, ***
    text = re.sub(r'_{1,2}', '', text)         # _, __
    text = re.sub(r'#{1,6}\s*', '', text)      # ### headers
    text = re.sub(r'~~', '', text)             # ~~strikethrough~~
    text = re.sub(r'`{1,3}', '', text)         # ` and ``` code blocks
    return text


def is_available() -> bool:
    return config.AI_ENABLED and bool(config.OPENAI_API_KEY)


async def ask(question: str) -> str:
    if not config.AI_ENABLED:
        return (
            "🤖 AI-режим выключен.\n"
            "Задай AI_ENABLED=true и OPENAI_API_KEY в .env для включения."
        )
    if not config.OPENAI_API_KEY:
        return "🤖 AI-режим не настроен: нет API-ключа (OPENAI_API_KEY в .env)."

    try:
        from openai import AsyncOpenAI

        kwargs: dict = {"api_key": config.OPENAI_API_KEY}
        if config.OPENAI_BASE_URL:
            kwargs["base_url"] = config.OPENAI_BASE_URL

        client = AsyncOpenAI(**kwargs)
        response = await client.chat.completions.create(
            model=config.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": _system_prompt()},
                {"role": "user", "content": question},
            ],
            max_tokens=600,
            temperature=0.4,
        )
        raw = response.choices[0].message.content or "Не удалось получить ответ."
        return _strip_markdown(raw)
    except Exception as exc:
        logger.error("AI request failed: %s", exc)
        return (
            "⚠️ Не удалось получить ответ от AI — попробуй позже.\n"
            "Используй меню для навигации по разделам."
        )
