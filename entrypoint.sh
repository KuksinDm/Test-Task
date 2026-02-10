#!/usr/bin/env bash
set -e

case "$1" in
  web)
    echo "Running migrations..."
    uv run python manage.py migrate

    echo "Initializing demo data..."
    uv run python manage.py start

    echo "Starting Django server..."
    exec uv run python manage.py runserver 0.0.0.0:8000
    ;;
  worker)
    echo "Starting Celery worker..."
    exec uv run celery -A config worker -l info
    ;;
  *)
    echo "Unknown command: $1"
    echo "Usage: entrypoint.sh [web|worker]"
    exit 1
    ;;
esac