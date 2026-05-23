# drone-rules-bot

Учебный проект 11 класса: Telegram-бот **«Правила управления дронами для начинающих»**.

## Что это

Telegram-бот-инструктор, который объясняет новичкам:

- подготовку к полёту;
- правила безопасности;
- запрещённые зоны (общие принципы + ссылки на официальные карты);
- регистрацию и закон (справочно);
- что делать при потере сигнала;
- советы новичкам;
- FAQ;
- полезные ссылки.

## Дисклеймер

Бот предоставляет **справочную** информацию. Это **не юридическая консультация**.
Все вопросы по регистрации, законам и запретным зонам нужно сверять с официальными источниками — см. [docs/SOURCES.md](docs/SOURCES.md).

## Статус

Stage 1 завершён — базовый бот с меню и статичной базой знаний работает.
Plan работ: [docs/TODO.md](docs/TODO.md). Текущее состояние: [docs/HANDOFF.md](docs/HANDOFF.md).

## Технологии

- Python 3.11+
- aiogram 3.x (Telegram Bot API, long polling)
- База знаний в YAML (`data/topics/`)
- Конфигурация через `.env`

## Как запустить локально

**Требования:** Python 3.11+, токен бота от [@BotFather](https://t.me/BotFather).

```bash
# 1. Клонировать репозиторий
git clone <repo-url>
cd drone-rules-bot

# 2. Создать виртуальное окружение и установить зависимости
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt

# 3. Настроить переменные окружения
cp .env.example .env
# Открой .env и вставь токен бота в TELEGRAM_BOT_TOKEN=

# 4. Запустить бота
python -m src.bot
```

Бот запущен — открой диалог с ним в Telegram и отправь `/start`.

## Smoke-тест (ручная проверка)

1. `/start` → приветствие + главное меню с 8 кнопками
2. Нажать каждую кнопку → получить текст раздела
3. Нажать «← Главное меню» → вернуться в меню
4. Отправить произвольный текст → получить предложение открыть меню
5. В разделах «Запрещённые зоны», «Регистрация», «FAQ» — виден дисклеймер

## Документы

- [CLAUDE.md](CLAUDE.md) — рамки работы Claude Code
- [AGENTS.md](AGENTS.md) — инструкции для Codex / агентов
- [docs/PROJECT_BRIEF.md](docs/PROJECT_BRIEF.md) — подробное описание
- [docs/ACCEPTANCE_CRITERIA.md](docs/ACCEPTANCE_CRITERIA.md) — критерии готовности
- [docs/DECISIONS.md](docs/DECISIONS.md) — технические решения
- [docs/HANDOFF.md](docs/HANDOFF.md) — текущее состояние
- [docs/TODO.md](docs/TODO.md) — этапы работ
- [docs/SOURCES.md](docs/SOURCES.md) — официальные источники
