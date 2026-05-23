# HANDOFF — текущее состояние проекта

> Обновляй этот файл после каждого Stage / значимого изменения. Это главный документ для входящего агента.

**Дата последнего обновления:** 2026-05-24
**Текущий Stage:** 4 — завершён. Готов к деплою на VPS.

---

## Goal

Создать рабочий Telegram-бот «Правила управления дронами для начинающих» как учебный проект 11 класса. Срок — около 1.5 дней. Должен выглядеть как нормальный продукт, временно поднят на сервере для защиты. Подробности — [PROJECT_BRIEF.md](PROJECT_BRIEF.md).

## Current State

Stage 4 завершён. Бот работает локально. Добавлены:
- Погодная функция «🌦 Погода для полёта» через Open-Meteo API (без ключа).
- Docker-деплой: `Dockerfile` + `docker-compose.yml`, запуск через `docker compose up -d --build`.
- Улучшен раздел «Запрещённые зоны»: конкретные ссылки на Росавиацию, Небосвод, DJI Fly Safe; явный дисклеймер «бот не определяет запретные зоны».
- Убраны ссылки на Airmap; добавлен Open-Meteo в links.yaml и SOURCES.md.

Готов к деплою на VPS.

## Completed

- **Stage 0:** документация и рамки проекта.
- **Stage 1:** базовый Telegram-бот (aiogram 3.x, 8 разделов, YAML база знаний).
- **Stage 2:** улучшенный контент и текстовый поиск.
- **Stage 3:** AI-режим через OpenAI-compatible API.
- **Stage 3.1 (hotfix):** AI-ответы без Markdown-мусора.
- **Stage 4:** погода + Docker.
  - `src/weather/__init__.py` + `src/weather/client.py` — Open-Meteo: геокодинг + прогноз, оценка условий, graceful degradation
  - `src/bot/handlers/weather.py` — FSM-хендлер `WeatherState.waiting_location`; поддержка города и координат (`lat, lon`); дисклеймер в каждом ответе
  - `src/bot/keyboards.py` — кнопка «🌦 Погода для полёта» (всегда видима, ключ не нужен)
  - `src/bot/__main__.py` — weather-роутер зарегистрирован перед common-роутером
  - `requirements.txt` — добавлен `aiohttp>=3.9`
  - `data/topics/restricted_zones.yaml` — улучшен текст, добавлены ссылки, убран Airmap
  - `data/topics/links.yaml` — убран Airmap, добавлен Небосвод и Open-Meteo
  - `Dockerfile` + `docker-compose.yml` — long polling, `env_file: .env`, `restart: unless-stopped`
  - `README.md` — разделы «Погодная проверка» и «Запуск через Docker»; обновлён smoke-тест
  - `docs/DECISIONS.md` — записи про Open-Meteo, aiohttp, Docker
  - `docs/SOURCES.md` — добавлены Open-Meteo (секция 7) и Небосвод (секция 9)

## Files in Flight

Нет. Все файлы Stage 4 завершены.

## Failed Attempts

Нет.

## Known Issues

- `docs/SOURCES.md` — большинство URL имеет статус «требует ручной проверки». Открой каждый перед защитой.
- Небосвод — URL не верифицирован в коде. В тексте бота написано «найди в браузере». Нужно найти актуальный URL перед защитой.
- Ограничение 4096 символов: все разделы в пределах нормы (проверить вручную при расширении).
- `MemoryStorage` — состояние сбрасывается при перезапуске бота. Для демо это ок.

## Decisions

См. полный журнал в [DECISIONS.md](DECISIONS.md).

## Next Step

**Деплой на VPS для защиты:**

1. Залить репозиторий на VPS (git clone или scp).
2. Скопировать `.env.example` → `.env`, вписать `TELEGRAM_BOT_TOKEN`.
3. `docker compose up -d --build`
4. `docker compose logs -f` — убедиться, что бот запустился.
5. Открыть Telegram, отправить `/start` — проверить меню.
6. Сделать screenshot/screencast на запасной случай.

## Notes for Next Agent

- Запуск бота: `python -m src.bot` из корня проекта.
- Структура YAML: `id`, `title`, `body`, `disclaimer` (опц.), `keywords` (список строк). Не менять структуру без записи в DECISIONS.md.
- Токен и ключи — только в `.env`, не в коде.
- AI-роутер и weather-роутер в `__main__.py` регистрируются **перед** common-роутером — это важно, иначе fallback перехватит FSM-сообщения.
- Open-Meteo не требует ключа — погода работает всегда.
- При смене провайдера AI — только `.env` (OPENAI_BASE_URL, OPENAI_MODEL, OPENAI_API_KEY).
