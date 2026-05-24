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

## Stage 3 — AI-режим ✅

Цель: добавить пункт меню «Спросить ИИ» через OpenAI-compatible API.

Переменные: `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_MODEL`, `AI_ENABLED`.

- [x] `src/ai/client.py` — обёртка над OpenAI-compatible API (библиотека `openai`)
- [x] `requirements.txt` — добавить `openai`
- [x] `.env.example` — добавить `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_MODEL`, `AI_ENABLED`
- [x] Системный промпт: запрет выдумывать законы, требование опираться на базу знаний
- [x] Контекст: title + keywords всех 8 топиков в системном промпте
- [x] `src/bot/keyboards.py` — кнопка «🤖 Спросить ИИ» в главном меню (только если `AI_ENABLED=true` и ключ задан)
- [x] Хендлер вопроса к AI с FSM (`AiState.waiting_question`, aiogram MemoryStorage)
- [x] Дисклеймер в каждом AI-ответе (через системный промпт)
- [x] Graceful degradation: при ошибке провайдера — «попробуйте позже», бот не падает
- [x] README: раздел «Настройка AI-режима», обновлён smoke-тест

---

## Stage 4 — Демонстрационный деплой ✅

Цель: бот доступен в Telegram во время защиты.

- [x] `src/weather/client.py` — погода через Open-Meteo (без ключа), геокодинг, оценка условий
- [x] `src/bot/handlers/weather.py` — FSM-хендлер, поддержка города и координат
- [x] `src/bot/keyboards.py` — кнопка «🌦 Погода для полёта»
- [x] `data/topics/restricted_zones.yaml` — улучшен текст, ссылки на регуляторов
- [x] `data/topics/links.yaml` — убран Airmap, добавлен Небосвод и Open-Meteo
- [x] `Dockerfile` + `docker-compose.yml` — long polling, restart: unless-stopped
- [x] README: разделы «Погодная проверка» и «Запуск через Docker»
- [x] `docs/DECISIONS.md` + `docs/SOURCES.md` обновлены
- [ ] Залить на VPS, запустить `docker compose up -d --build`
- [ ] Прописать `TELEGRAM_BOT_TOKEN` на сервере
- [ ] Проверить через Telegram (smoke-тест)
- [ ] Сделать screenshot/screencast на запасной случай

---

## Stage 5 — Финальная полировка ✅

Цель: UX-полировка, мини-тест, обратная связь, обновление документов перед защитой.

- [x] `src/bot/handlers/weather.py` — FSM не сбрасывается при ошибке (не_найдено / недоступно); пользователь может сразу повторить ввод
- [x] `src/bot/handlers/quiz.py` — мини-тест: 5 вопросов, inline-кнопки, ✅/❌ после каждого ответа, итог X/5
- [x] `src/bot/handlers/feedback.py` — FSM «Оставить вопрос»; сохраняет только текст + время в `logs/feedback.txt`; личные данные не сохраняются
- [x] `src/bot/keyboards.py` — кнопка «🧠 Мини-тест» в главном меню; `feedback_no_result_kb()`
- [x] `src/bot/handlers/common.py` — fallback no-result использует `feedback_no_result_kb`
- [x] `src/bot/__main__.py` — зарегистрированы роутеры quiz и feedback
- [x] `.gitignore` — добавлен `logs/`
- [x] `README.md` — раздел «Что реализовано», сценарий демонстрации, обновлён smoke-тест
- [x] `docs/TODO.md`, `docs/HANDOFF.md`, `docs/DECISIONS.md` обновлены

---

## Stage 6 — Документация и GitHub-polish ✅

Цель: сделать репозиторий понятным для GitHub, заказчика и нового разработчика. Код бота не менять.

- [x] `README.md` полностью переработан: оглавление, скриншот-плейсхолдеры, описание всех функций, структура меню/проекта, запуск (локально + Docker), сценарий демонстрации, smoke-тест, безопасность, дисклеймер, источники, улучшения
- [x] `.env.example` улучшен: пример Polza AI (`OPENAI_BASE_URL=https://polza.ai/api/v1`, `OPENAI_MODEL=google/gemini-3.1-flash-lite`), placeholder вместо пустого ключа, расширенные комментарии
- [x] `docs/ENVIRONMENT.md` — переменные окружения, примеры Polza AI / OpenAI / других OpenAI-compatible
- [x] `docs/DEPLOYMENT.md` — деплой на VPS через Docker (установка Docker, заливка, .env, обновление, типовые проблемы)
- [x] `docs/DEMO_SCENARIO.md` — сценарий показа на 7 шагов + ожидаемые вопросы комиссии
- [x] `docs/MAINTENANCE.md` — карта «что где лежит», типовые задачи, чего не делать, чек-лист перед коммитом
- [x] `docs/HANDOFF.md` обновлён — Stage 6 завершён, current state = ready, next step = только деплой/скриншоты
- [x] `docs/TODO.md` обновлён — основная разработка завершена, backlog оставлен
- [x] Проверена GitHub-гигиена: `.env`, `logs/`, `__pycache__`, `.venv` в `.gitignore`; реальных секретов в репозитории нет

---

## Основная разработка завершена

Дальнейшие изменения — только багфиксы или доработки по обратной связи от заказчика/преподавателя.

## Backlog / nice-to-have

- Скриншоты в `docs/screenshots/` (плейсхолдер уже есть в README).
- Презентация к защите.
- Расширение FAQ (новые частые вопросы).
- Уточнение карты запретных зон (только ссылки на официальные источники).
- Локализация (RU/EN).
- Inline-режим в Telegram.
- Минимальные тесты для парсера базы знаний и поиска.
- Метрики использования (без персональных данных).
- Простая админка для просмотра `logs/feedback.txt` через защищённый эндпоинт.
