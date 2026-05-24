# ENVIRONMENT — переменные окружения

Все настройки бота передаются через `.env` в корне проекта.
Шаблон — [`.env.example`](../.env.example). Реальные значения коммитить **нельзя** — `.env` находится в `.gitignore`.

---

## Полный список переменных

| Переменная | Обязательная | Назначение |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | да | Токен Telegram-бота от [@BotFather](https://t.me/BotFather). |
| `AI_ENABLED` | нет | `true` / `false`. Включает кнопку «🤖 Спросить ИИ». По умолчанию `false`. |
| `OPENAI_API_KEY` | нет | API-ключ провайдера. Требуется только если `AI_ENABLED=true`. |
| `OPENAI_BASE_URL` | нет | Base URL OpenAI-compatible провайдера. Пусто = OpenAI по умолчанию. |
| `OPENAI_MODEL` | нет | Название модели у провайдера. По умолчанию `gpt-4o-mini`. |
| `LOG_LEVEL` | нет | `DEBUG` / `INFO` / `WARNING` / `ERROR`. По умолчанию `INFO`. |

---

## Минимальный `.env` (без AI)

```env
TELEGRAM_BOT_TOKEN=1234567890:AA-your-token-here
AI_ENABLED=false
LOG_LEVEL=INFO
```

При такой конфигурации бот работает полноценно: все 8 разделов, поиск, погода, мини-тест, обратная связь. Кнопка «🤖 Спросить ИИ» не показывается.

---

## Пример для Polza AI

[Polza AI](https://polza.ai) — OpenAI-compatible провайдер, через который доступны разные модели одним ключом.

```env
TELEGRAM_BOT_TOKEN=1234567890:AA-your-token-here

AI_ENABLED=true
OPENAI_API_KEY=your_polza_key_here
OPENAI_BASE_URL=https://polza.ai/api/v1
OPENAI_MODEL=google/gemini-3.1-flash-lite

LOG_LEVEL=INFO
```

> ⚠️ Реальный ключ в README/`.env.example`/коде хранить запрещено. Подставлять только в локальный `.env` на машине или на VPS.

---

## Пример для OpenAI

```env
TELEGRAM_BOT_TOKEN=1234567890:AA-your-token-here

AI_ENABLED=true
OPENAI_API_KEY=sk-...
OPENAI_BASE_URL=
OPENAI_MODEL=gpt-4o-mini

LOG_LEVEL=INFO
```

При пустом `OPENAI_BASE_URL` библиотека `openai` использует стандартный endpoint OpenAI.

---

## Другие OpenAI-compatible провайдеры

Любой провайдер, реализующий OpenAI Chat Completions API, подходит. Достаточно подставить три поля:

```env
OPENAI_API_KEY=<ключ провайдера>
OPENAI_BASE_URL=<base URL провайдера, обычно заканчивается на /v1>
OPENAI_MODEL=<название модели у провайдера>
```

Код бота переключать не нужно — см. [`src/ai/client.py`](../src/ai/client.py).

---

## Как переменные используются

- Загружаются в [`src/config.py`](../src/config.py) через `python-dotenv`.
- Кнопка «🤖 Спросить ИИ» появляется в меню только при `AI_ENABLED=true` **и** непустом `OPENAI_API_KEY` (см. [`src/bot/keyboards.py:24`](../src/bot/keyboards.py)).
- Если AI-провайдер вернёт ошибку, бот ответит «попробуй позже» и продолжит работать — остальное меню не ломается.

---

## Безопасность

- `.env` находится в [`.gitignore`](../.gitignore) — случайно закоммитить не получится.
- Если ключ всё же попал в git: **отозви его у провайдера**, замени на новый, перепиши историю (`git filter-repo` / новый репозиторий).
- На VPS храни `.env` с правами `chmod 600`.
- Не выкладывай скриншоты с открытым токеном/ключом.
