import os
from django.core.management.base import BaseCommand
from users.models import User


NAME = "users"


class Command(BaseCommand):

    help = f"This command creates super user"

    def handle(self, *args, **options):

        admin = User.objects.get_or_none(username="ebadmin")
        if admin is None:
            User.objects.create_superuser(
                "ebadmin", os.environ.get("SU_EMAIL"), os.environ.get("SU_PASSWORD")
            )
            self.stdout.write(self.style.SUCCESS(f"Super user created"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Super user already exists"))
