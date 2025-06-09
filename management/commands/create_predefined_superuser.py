# your_app_name/management/commands/create_predefined_superuser.py

import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a superuser with predefined credentials from environment variables'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not username or not password:
            self.stdout.write(self.style.ERROR(
                'Environment variables DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD must be set.'
            ))
            return

        if not User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(f"Creating superuser '{username}'"))
            User.objects.create_superuser(
                username=username,
                password=password,
                email=f"{username}@example.com"  # Optional: create a dummy email
            )
        else:
            self.stdout.write(self.style.WARNING(f"Superuser '{username}' already exists. Skipping creation."))