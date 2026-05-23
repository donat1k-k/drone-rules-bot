# TODO — этапы работ

Один Stage за раз. После завершения Stage — обновить [HANDOFF.md](HANDOFF.md), отметить тут, перейти к следующему.

---

## Stage 0 — Документация и рамки ✅

- [x] CLAUDE.md
- [x] AGENTS.md
- [x] README.md
- [x] .env.example
- [x] docs/PROJECT_BRIEF.md
- [x] docs/ACCEPTANCE_CRITERIA.md
- [x] docs/HANDOFF.md
- [x] docs/DECISIONS.md
- [x] docs/TODO.md
- [x] docs/SOURCES.md (каркас, ссылки заполняются по ходу)

---

## Stage 1 — Базовый Telegram-бот ✅

- [x] `requirements.txt`: `aiogram>=3.4`, `python-dotenv`, `PyYAML`
- [x] `.gitignore` с `.env`, `__pycache__/`, `.venv/`
- [x] `src/config.py` — чтение env (`TELEGRAM_BOT_TOKEN`, `LOG_LEVEL`)
- [x] `src/bot/__main__.py` — entrypoint, long polling (`await dp.start_polling(bot)`)
- [x] Хендлеры: `/start`, `/help`, главное меню (inline-кнопки)
- [x] Хендлеры разделов: подготовка, безопасность, запретные зоны, регистрация, потеря сигнала, советы, FAQ, ссылки
- [x] Кнопка «Назад в меню» в каждом разделе
- [x] `src/knowledge/` — загрузка статей из `data/topics/*.yaml`
- [x] `data/topics/*.yaml` — тексты для всех 8 разделов
- [x] Дисклеймер в юридических разделах (restricted_zones, registration, faq)
- [x] README: раздел «Как запустить локально»
- [x] Smoke-тест: описан в README

---

## Stage 2 — Улучшенный контент и текстовый поиск ✅

- [x] FAQ расширен до 11 вопросов-ответов
- [x] Полезные ссылки: 6 рабочих URL (Росавиация, Госуслуги, ИКАО, DJI Fly Safe, Airmap, Windy)
- [x] Все 8 YAML-топиков: добавлено поле `keywords`, улучшено форматирование
- [x] Юридические разделы: аккуратные формулировки, дисклеймер сохранён
- [x] `docs/SOURCES.md` — заполнены секции 2, 3, 4 с пометками «требует ручной проверки»
- [x] `src/knowledge/search.py` — простой keyword-поиск по базе знаний
- [x] `src/bot/keyboards.py` — добавлена `search_result_kb`
- [x] `src/bot/handlers/common.py` — fallback использует поиск; `/help` объясняет текстовый ввод
- [x] README обновлён: поиск, AI статус, актуальный smoke-тест

---

## Stage 3 — AI-режим (опционально, если останется время)

Цель: добавить пункт меню «Спросить ИИ» через OpenAI-compatible API.

Переменные: `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_MODEL`, `AI_ENABLED`.

- [ ] `src/ai/client.py` — обёртка над OpenAI-compatible API (библиотека `openai`)
- [ ] `requirements.txt` — добавить `openai`
- [ ] `.env.example` — добавить `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_MODEL`, `AI_ENABLED`
- [ ] Системный промпт: запрет выдумывать законы, требование опираться на базу знаний
- [ ] Контекст: загрузка содержимого YAML-топиков в системный промпт
- [ ] `src/bot/keyboards.py` — кнопка «🤖 Спросить ИИ» в главном меню (только если `AI_ENABLED=true`)
- [ ] Хендлер вопроса к AI и возврата ответа
- [ ] Дисклеймер в каждом AI-ответе
- [ ] Graceful degradation: при ошибке провайдера — «попробуйте позже», бот не падает
- [ ] README: обновить раздел статуса и smoke-тест

---

## Stage 4 — Демонстрационный деплой

Цель: бот доступен в Telegram во время защиты.

- [ ] Выбрать хостинг (Railway / Render / VPS).
- [ ] Прописать переменные окружения на хостинге.
- [ ] Запустить и проверить через Telegram.
- [ ] README: раздел «Деплой» с шагами.
- [ ] Сделать screenshot/screencast на запасной случай.
- [ ] (Опционально) Dockerfile.

---

## Backlog / nice-to-have

- Локализация (RU/EN).
- Inline-режим в Telegram.
- Минимальные тесты для парсера базы знаний и поиска.
- Метрики использования (без персональных данных).
