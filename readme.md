# Info Map Project

Проект для управления организациями, зданиями и видами деятельности.

---

## 🚀 Установка и запуск через Docker

### 1. Клонируем репозиторий

```bash
git clone https://github.com/VaDKo61/17.-info_map
cd 17.-info_map
```

### 2. Настройка `.env_template`

По умолчанию API key:
- APP_CONFIG__API_KEY=1

### 3. Запуск через Docker Compose

```bash
docker-compose up --build
```

- `db` — PostgreSQL
- `backend` — FastAPI

Swagger будет доступно на `http://localhost:8000/docs`.

---

## 🛠 Создание таблиц и заполнение базы (Seed)

В контейнере `backend`:

```bash
docker exec -it info_map_backend bash
alembic upgrade head
python seed.py
```