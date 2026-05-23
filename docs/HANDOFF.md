# HANDOFF — текущее состояние проекта

> Обновляй этот файл после каждого Stage / значимого изменения. Это главный документ для входящего агента.

**Дата последнего обновления:** 2026-05-23
**Текущий Stage:** 1 — завершён. Готов к Stage 2.

---

## Goal

Создать рабочий Telegram-бот «Правила управления дронами для начинающих» как учебный проект 11 класса. Срок — около 1.5 дней. Должен выглядеть как нормальный продукт, временно поднят на сервере для защиты. Подробности — [PROJECT_BRIEF.md](PROJECT_BRIEF.md).

## Current State

Stage 1 завершён. Бот работает локально: `/start`, `/help`, 8 разделов через inline-меню, кнопки возврата, fallback на неизвестные сообщения. Контент загружается из YAML-файлов. AI-режим не реализован (по плану Stage 3). Docker и деплой — позже.

## Completed

- **Stage 0:** документация и рамки проекта (см. предыдущий HANDOFF).
- **Stage 1:** базовый Telegram-бот.
  - `requirements.txt` — `aiogram>=3.4`, `python-dotenv`, `PyYAML`
  - `.gitignore` — исключает `.env`, `__pycache__/`, `.venv/`
  - `src/config.py` — загрузка `TELEGRAM_BOT_TOKEN`, `LOG_LEVEL` из `.env`
  - `src/knowledge/loader.py` — загрузка и кэширование YAML-топиков
  - `src/bot/keyboards.py` — `main_menu_kb()`, `back_kb()`
  - `src/bot/handlers/common.py` — `/start`, `/help`, `menu` callback, fallback
  - `src/bot/handlers/topics.py` — обработчик всех 8 разделов по `topic:<id>`
  - `src/bot/__main__.py` — entrypoint, `await dp.start_polling(bot)`
  - `data/topics/*.yaml` — 8 файлов базы знаний (preparation, safety, restricted_zones, registration, signal_loss, tips, faq, links)
  - `README.md` — обновлён, добавлен раздел «Как запустить локально»
  - `docs/SOURCES.md` — заполнены ссылки на Росавиацию, Госуслуги, ИКАО, Windy, DJI Fly Safe

## Changed This Session (Stage 1)

- Создана вся структура `src/` и `data/`.
- Написан рабочий бот на aiogram 3.x с long polling.
- Заполнены тексты всех 8 разделов базы знаний.
- Юридические разделы (restricted_zones, registration, faq) содержат дисклеймер.
- AI-режим не реализован: пункта «Спросить ИИ» в меню нет.

## Files in Flight

Нет. Все файлы Stage 1 дописаны.

## Failed Attempts

Нет.

## Known Issues

- `docs/SOURCES.md` — заполнены только 3 из 8 позиций (Росавиация, ИКАО, Windy). Секции 2, 3, 4 по-прежнему `_TBD_`. Заполнить на Stage 2.
- Тексты в YAML — черновые. Stage 2 — довести до качества демо.
- FAQ содержит 7 вопросов, ссылки — 6 пунктов (выше минимума по acceptance criteria).
- `data/topics/links.yaml` — ссылка на Госуслуги без прямого URL услуги. Уточнить на Stage 2.
- Ограничение 4096 символов на сообщение: текущие тексты укладываются, но при расширении Stage 2 нужно следить.

## Decisions

См. полный журнал в [DECISIONS.md](DECISIONS.md). Новых решений в Stage 1 не принималось.

## Next Step

**Stage 2 — Полный контент.**

Конкретно для входящего агента:

1. Прочитать [AGENTS.md](../AGENTS.md), [TODO.md](TODO.md) (раздел Stage 2), [ACCEPTANCE_CRITERIA.md](ACCEPTANCE_CRITERIA.md) разделы B, C, H.
2. Заполнить `docs/SOURCES.md` — найти реальные URL для секций 2 (нормативные акты), 3 (карта зон), 4 (подача плана полёта).
3. Улучшить тексты разделов подготовки, безопасности, потери сигнала, советов.
4. Уточнить формулировки в юридических разделах, сверить с источниками из SOURCES.md.
5. Найти прямой URL услуги постановки на учёт БВС на Госуслугах.
6. Проверить, что длинные разделы не превышают 4096 символов.
7. Обновить этот HANDOFF.md и отметить Stage 2 в TODO.md.

Чего **не делать** на Stage 2: AI-интеграцию, Dockerfile, деплой, рефакторинг кода.

## Notes for Next Agent

- Запуск бота: `python -m src.bot` из корня проекта.
- Структура YAML: `id`, `title`, `body`, `disclaimer` (опционально). Не менять структуру без записи в DECISIONS.md.
- Токен бота — только в `.env`, не в коде.
- AI-режим — Stage 3, не трогать сейчас.
- Если добавляешь ссылки в `data/topics/links.yaml` — дублируй в `docs/SOURCES.md`.
