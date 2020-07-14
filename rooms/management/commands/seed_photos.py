import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User
from rooms import models

NAME = "rooms"


class Command(BaseCommand):

    help = f"This command creates many {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            type=int,
            default=1,
            help=f"How many {NAME} do you want to create",
        )

    def handle(self, *args, **options):

        number = options.get("number")
        seeder = Seed.seeder()
        user = User.objects.get(pk=number)
        room = models.Room.objects.get(pk=50)
        for num in range(3):
            models.Photo.objects.create(
                caption=seeder.faker.sentence(),
                file=f"rooms_photo/{random.randint(1, 25)}.webp",
                room=room,
            )

        self.stdout.write(self.style.SUCCESS(f"3 Photos created"))
