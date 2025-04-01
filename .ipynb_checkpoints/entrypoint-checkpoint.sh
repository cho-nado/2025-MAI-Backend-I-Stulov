#!/bin/bash
set -e

# echo "Running migrations..."
# Если надо автоматизировать миграцию (но обычно миграции запускают отдельно)
# python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Copying static files to /usr/share/nginx/html..."
cp -R /app/schoolmind/public/* /usr/share/nginx/html/

echo "Starting Gunicorn..."
exec gunicorn schoolmind.wsgi:application --bind 0.0.0.0:8000
