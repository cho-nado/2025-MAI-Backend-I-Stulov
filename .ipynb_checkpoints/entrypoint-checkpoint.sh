#!/bin/bash
set -e

echo "Collecting static files..."
cd schoolmind
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn schoolmind.wsgi:application --bind 0.0.0.0:8000
