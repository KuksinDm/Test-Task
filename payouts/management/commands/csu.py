import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = (
        "Создаёт суперпользователя из переменных окружения "
        "SUPERUSER_USERNAME и SUPERUSER_PASSWORD"
    )

    def handle(self, *args, **options):
        username = os.getenv("SUPERUSER_USERNAME")
        password = os.getenv("SUPERUSER_PASSWORD")
        email = os.getenv("SUPERUSER_EMAIL", "")

        if not username or not password:
            raise CommandError(
                "Нужно указать SUPERUSER_USERNAME и SUPERUSER_PASSWORD в .env"
            )

        User = get_user_model()

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(
                    f"ℹ️ Суперпользователь с username '{username}' уже существует"
                )
            )
            return

        user = User.objects.create_superuser(
            username=username,
            password=password,
            email=email,
        )
        self.stdout.write(
            self.style.SUCCESS(f"✅ Суперпользователь создан: {user.username}")
        )
