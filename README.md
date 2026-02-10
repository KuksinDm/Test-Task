# Test-Task

REST сервис для управления заявками на выплату средств с асинхронной
обработкой через Celery и Redis.

## Быстрый старт (локально)
```bash
uv venv
uv sync
python manage.py migrate
python manage.py start
python manage.py runserver
```

## Запуск в Docker
```bash
docker compose up --build
```

После старта:
- API: `http://localhost:8000/api/payouts/`
- Swagger: `http://localhost:8000/api/docs/`
- Redoc: `http://localhost:8000/api/redoc/`

## Команды
```bash
python manage.py migrate
python manage.py start          # суперпользователь + мок-данные
python manage.py load_mock_data # только мок-данные
pytest
```

## Celery
Локально:
```bash
celery -A config worker -l info
```

В Docker запускается отдельный сервис `celery_worker_test_task`.

## Переменные окружения
Ключевые переменные в `.env`:
```
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
POSTGRES_DB=test_db
POSTGRES_USER=test_user
POSTGRES_PASSWORD=test_password
POSTGRES_HOST=test_db
POSTGRES_PORT=5432
CELERY_BROKER_URL=redis://redis:6379/0
SUPERUSER_USERNAME=admin
SUPERUSER_PASSWORD=admin
```

## Деплой (кратко)
- Контейнеризовать web + worker, отдельные сервисы Postgres и Redis.
- Django запускать через `gunicorn`, Celery через `celery worker`.
- Использовать env vars для конфигурации, миграции выполнять при деплое.
- Логи собирать через stdout/centralized logging.