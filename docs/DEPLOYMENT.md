# DEPLOYMENT — деплой на VPS через Docker

Бот работает через **long polling**, поэтому HTTPS-домен, webhook и nginx **не нужны**. Достаточно любого VPS с Docker.

---

## Требования

- VPS на Linux (Ubuntu 22.04 / Debian 12 — проверено).
- Docker Engine + плагин `docker compose v2`.
- Открытый исходящий доступ в интернет (Telegram API, Open-Meteo, AI-провайдер).
- Токен бота от [@BotFather](https://t.me/BotFather).

Установка Docker на чистый Ubuntu:

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
# перезайди в SSH или: newgrp docker
```

---

## Деплой по шагам

### 1. Залить код на VPS

```bash
git clone <url-репозитория> drone-rules-bot
cd drone-rules-bot
```

### 2. Создать и заполнить `.env`

```bash
cp .env.example .env
nano .env   # или vim/vi
```

Минимально подставь `TELEGRAM_BOT_TOKEN`. Опционально — переменные AI (см. [ENVIRONMENT.md](ENVIRONMENT.md)).

Закрой доступ к файлу:

```bash
chmod 600 .env
```

### 3. Собрать образ и запустить

```bash
docker compose up -d --build
```

Флаги:
- `-d` — фоном (detached).
- `--build` — пересобрать образ перед запуском.

### 4. Проверить логи

```bash
docker compose logs -f
```

В логах должна появиться строка о подключении aiogram к Telegram API. `Ctrl+C` — выход из просмотра (бот продолжит работать).

### 5. Проверить в Telegram

Открой диалог с ботом → `/start` → проверь, что меню показывается. Прогон smoke-теста — см. [README.md](../README.md#smoke-тест-ручная-проверка).

---

## Обслуживание

### Остановить

```bash
docker compose down
```

### Перезапустить

```bash
docker compose restart
```

### Обновить код (после `git pull`)

```bash
git pull
docker compose up -d --build
```

`--build` пересоберёт образ с новым кодом, `up -d` подменит контейнер без простоя меню в Telegram (краткий разрыв polling).

### Автозапуск после ребута сервера

В [`docker-compose.yml`](../docker-compose.yml) задано `restart: unless-stopped` — контейнер поднимается автоматически вместе с Docker. Дополнительной настройки systemd не нужно.

---

## Где смотреть обратную связь от пользователей

Файл `logs/feedback.txt` создаётся внутри контейнера. Чтобы получить с хоста:

```bash
docker compose cp bot:/app/logs/feedback.txt ./feedback.txt
```

Хранится только текст вопроса + время. user_id / username не сохраняются.

> Если нужна персистентность между пересборками, добавь том в `docker-compose.yml`:
> ```yaml
> volumes:
>   - ./logs:/app/logs
> ```
> (это уже изменение архитектуры — фиксируй в `docs/DECISIONS.md`).

---

## Типовые проблемы

| Симптом | Причина / решение |
|---|---|
| `TELEGRAM_BOT_TOKEN is not set` при старте | Пустой или некорректный `.env`. Проверь `cat .env`. |
| Бот не отвечает на `/start` | Проверь логи: `docker compose logs --tail=50`. Возможно, токен неверный или сеть VPS блокирует Telegram. |
| Кнопка «🤖 Спросить ИИ» отсутствует | Это норма при `AI_ENABLED=false` или пустом `OPENAI_API_KEY`. |
| Погода не отвечает | Проверь, что VPS имеет доступ к `api.open-meteo.com` (без VPN / прокси). |
| Контейнер постоянно перезапускается | `docker compose logs` — смотри traceback, чаще всего проблема в `.env`. |

---

## Альтернативы Docker

Если Docker недоступен, можно запустить напрямую (см. [README.md](../README.md#быстрый-запуск-локально)) и обернуть в `systemd`-сервис. Это вне scope учебного проекта, но технически работает.
