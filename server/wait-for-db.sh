#!/bin/sh

until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  echo "Waiting for postgres..."
  sleep 2
done

