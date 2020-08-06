import os
from django.core.management.base import BaseCommand
from users.models import User


NAME = "users"


class Command(BaseCommand):

    help = f"This command creates super user"

    def handle(self, *args, **options):

        try:
            User.objects.get(username="ebadmin")
            self.stdout.write(self.style.SUCCESS(f"Super user already exists"))
        except User.DoesNotExist:
            User.objects.create_superuser(
                "ebadmin", os.environ.get("SU_EMAIL"), os.environ.get("SU_PASSWORD")
            )
            self.stdout.write(self.style.SUCCESS(f"Super user created"))
