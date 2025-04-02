from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Create a default superuser'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        
        username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD', '12345')

        if User.objects.filter(username=username).exists():
            self.stdout.write('Superuser already exists.')
        else:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(f'Superuser "{username}" created.')
