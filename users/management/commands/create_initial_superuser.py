# backend/users/management/commands/create_initial_superuser.py

import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

# --- THIS IS THE CRITICAL LINE ---
# The class MUST be named 'Command' and it MUST inherit from BaseCommand.
class Command(BaseCommand):
    help = 'Creates a superuser with predefined credentials from environment variables'

    def handle(self, *args, **options):
        # This is the logic that will be executed.
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
                email=f"{username}@example.com"
            )
        else:
            self.stdout.write(self.style.WARNING(f"Superuser '{username}' already exists. Skipping creation."))