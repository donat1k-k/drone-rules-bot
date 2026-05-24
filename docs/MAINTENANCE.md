# MAINTENANCE — как поддерживать и дорабатывать проект

Карта проекта для человека, который не писал этот код, но должен его поддерживать или расширять.

---

## Карта «что где лежит»

| Что хочешь изменить | Файл / каталог |
|---|---|
| Текст любого раздела (правила, FAQ, ссылки) | [`data/topics/*.yaml`](../data/topics/) |
| Кнопки главного меню | [`src/bot/keyboards.py`](../src/bot/keyboards.py) |
| Логику AI-режима, системный промпт | [`src/ai/client.py`](../src/ai/client.py) |
| Логику погоды (оценка, источники) | [`src/weather/client.py`](../src/weather/client.py) |
| Вопросы мини-теста | [`src/bot/handlers/quiz.py`](../src/bot/handlers/quiz.py) |
| Обработку обратной связи | [`src/bot/handlers/feedback.py`](../src/bot/handlers/feedback.py) |
| Поведение fallback (нераспознанный вопрос) | [`src/bot/handlers/common.py`](../src/bot/handlers/common.py) |
| Поиск по базе знаний | [`src/knowledge/search.py`](../src/knowledge/search.py) |
| Загрузку YAML | [`src/knowledge/loader.py`](../src/knowledge/loader.py) |
| Конфиг (`.env` → Python) | [`src/config.py`](../src/config.py) |
| Деплой (Docker) | [`Dockerfile`](../Dockerfile), [`docker-compose.yml`](../docker-compose.yml) |
| Точка входа бота | [`src/bot/__main__.py`](../src/bot/__main__.py) |
| Переменные окружения | [`.env`](../.env) (локальный, не в git) + [`.env.example`](../.env.example) |
| Текущий статус проекта | [`docs/HANDOFF.md`](HANDOFF.md) |
| История технических решений | [`docs/DECISIONS.md`](DECISIONS.md) |
| Официальные источники | [`docs/SOURCES.md`](SOURCES.md) |

---

## Типовые задачи

### Изменить текст раздела

1. Открой нужный файл в `data/topics/*.yaml`.
2. Поправь `body`. Структуру (`id`, `title`, `body`, `disclaimer`, `keywords`) не меняй.
3. Перезапусти бот (`docker compose restart` или `Ctrl+C` + повторный запуск).

### Добавить новый раздел в меню

1. Создай `data/topics/<id>.yaml` по структуре существующих файлов.
2. Добавь `(label, "topic:<id>")` в список `_SECTIONS` в [`src/bot/keyboards.py:6`](../src/bot/keyboards.py).
3. Добавь `<id>` в список `_TOPIC_IDS` в [`src/ai/client.py:11`](../src/ai/client.py) — чтобы AI знал о новом разделе.
4. Перезапусти бот.

> Хендлер `topics.py` уже универсальный — отдельный код под раздел писать не нужно.

### Добавить вопрос в мини-тест

Открой [`src/bot/handlers/quiz.py`](../src/bot/handlers/quiz.py). Найди список вопросов (`QUESTIONS` или аналогичный). Добавь объект по тому же шаблону: `question`, варианты ответов, индекс правильного, объяснение.

### Поменять AI-провайдера

**Код менять не надо.** В `.env`:

```env
OPENAI_API_KEY=<ключ нового провайдера>
OPENAI_BASE_URL=<base URL нового провайдера>
OPENAI_MODEL=<модель нового провайдера>
```

Перезапусти бот. Подробнее — [ENVIRONMENT.md](ENVIRONMENT.md).

### Изменить порог оценки погоды

[`src/weather/client.py:90`](../src/weather/client.py), функция `_assess`. По умолчанию:
- ветер ≥ 10 м/с **или** есть осадки → ⛔
- ветер 5–9.9 м/с → ⚠️
- иначе → ✅

### Изменить системный промпт AI

[`src/ai/client.py:16`](../src/ai/client.py), переменная `_SYSTEM_PROMPT_TEMPLATE`.

> ⚠️ Не убирай блок «СТРОГИЕ ПРАВИЛА» — он удерживает AI от выдумывания законов. См. [`CLAUDE.md`](../CLAUDE.md) раздел 4.

### Изменить дисклеймер

Если в конкретном разделе — поле `disclaimer` в `data/topics/<id>.yaml`.
Если в AI-ответах — пункт 5 системного промпта в [`src/ai/client.py`](../src/ai/client.py).

---

## Чего НЕ делать

- Не выдумывать номера статей, суммы штрафов, точные веса для регистрации, если их нет в [SOURCES.md](SOURCES.md).
- Не убирать дисклеймеры из юридических разделов (запрещённые зоны, регистрация, FAQ).
- Не коммитить `.env`, токены, ключи.
- Не добавлять собственную «карту запретных зон» — только ссылки на официальные источники.
- Не вводить БД пользователей без обновления `docs/DECISIONS.md` — это смена архитектуры.
- Не менять структуру YAML (`id`, `title`, `body`, `disclaimer`, `keywords`) без обновления `loader.py` и записи в `DECISIONS.md`.

---

## Перед коммитом — чек-лист

- [ ] Нет реальных токенов / ключей в diff.
- [ ] `.env` не в стейдже (`git status` это покажет).
- [ ] В юридических разделах дисклеймер на месте.
- [ ] Бот стартует локально (`python -m src.bot`) без ошибок.
- [ ] Если поменялась архитектура — запись в [`docs/DECISIONS.md`](DECISIONS.md).
- [ ] Если поменялся статус — обновлён [`docs/HANDOFF.md`](HANDOFF.md).

---

## Куда смотреть после клонирования

1. [README.md](../README.md) — что это и как запустить.
2. [docs/HANDOFF.md](HANDOFF.md) — текущее состояние, что было сделано, что дальше.
3. [docs/DECISIONS.md](DECISIONS.md) — почему сделано именно так.
4. [docs/PROJECT_BRIEF.md](PROJECT_BRIEF.md) — суть проекта, scope, антикоп.
5. [docs/ACCEPTANCE_CRITERIA.md](ACCEPTANCE_CRITERIA.md) — критерии готовности.
