#!/bin/bash
set -e

# echo "Running migrations..."
# Если надо автоматизировать миграцию (но обычно миграции запускают отдельно)
# python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

# echo "Copying static files to /usr/share/nginx/html..."
# cp -R /app/schoolmind/public/* /usr/share/nginx/html/

# echo "Creating superuser if not exists..."
# python manage.py shell <<EOF
# from django.contrib.auth import get_user_model 
# User = get_user_model() 
# username = '${DJANGO_SUPERUSER_USERNAME}' 
# email = '${DJANGO_SUPERUSER_EMAIL}' 
# password = '${DJANGO_SUPERUSER_PASSWORD}' 
# if not User.objects.filter(username=username).exists(): 
#     print("Creating superuser...") 
#     User.objects.create_superuser(username, email, password) 
# else: 
#     print("Superuser already exists.")
# EOF

# echo "Superuser details: username=${DJANGO_SUPERUSER_USERNAME}, email=${DJANGO_SUPERUSER_EMAIL}"


echo "Starting Gunicorn..."
exec gunicorn schoolmind.wsgi:application --bind 0.0.0.0:8000
