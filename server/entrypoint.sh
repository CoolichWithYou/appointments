#!/bin/bash
set -e

host=$(echo $DATABASE_URL | sed -E 's/.*@([^:/]+).*/\1/')
port=$(echo $DATABASE_URL | sed -E 's/.*:([0-9]+)\/.*/\1/')

until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  echo "Waiting for postgres..."
  sleep 2
done

echo "Применение миграции из /versions"
alembic -c /server/alembic.ini upgrade head

echo "Запуск сервера"
exec uvicorn server.main:app --host 0.0.0.0 --port 8000
