import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from lists import models as list_models
from users import models as user_models
from rooms import models as room_models

NAME = "lists"


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
        all_users = user_models.User.objects.all()
        seeder.add_entity(
            list_models.List, number, {"user": lambda x: random.choice(all_users)}
        )
        created_lists_pk = seeder.execute()
        created_pk_clean = sum(list(created_lists_pk.values()), [])
        rooms = room_models.Room.objects.all()
        for pk in created_pk_clean:
            list_instance = list_models.List.objects.get(pk=pk)
            for r in rooms:
                if random.randint(1, 15) % 2 == 0:
                    list_instance.room.add(r)

        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created"))
