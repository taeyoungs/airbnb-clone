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
        all_users = User.objects.all()
        room_types = models.RoomType.objects.all()
        seeder.add_entity(
            models.Room,
            number,
            {
                "name": lambda x: seeder.faker.address(),
                "price": lambda x: random.randint(100, 300),
                "guests": lambda x: random.randint(1, 20),
                "beds": lambda x: random.randint(1, 5),
                "bath": lambda x: random.randint(1, 5),
                "bedrooms": lambda x: random.randint(1, 5),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
            },
        )
        created_rooms_pk = seeder.execute()
        created_pk_clean = sum(list(created_rooms_pk.values()), [])
        amenities = models.Amenity.objects.all()
        facilities = models.Facility.objects.all()
        house_rules = models.HouseRule.objects.all()
        for pk in created_pk_clean:
            room = models.Room.objects.get(pk=pk)
            for num in range(3, random.randint(15, 25)):
                models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    file=f"rooms_photo/{random.randint(1, 25)}.webp",
                    room=room,
                )
            for a in amenities:
                if random.randint(1, 15) % 2 == 0:
                    room.amenity.add(a)
            for f in facilities:
                if random.randint(1, 15) % 2 == 0:
                    room.facility.add(f)
            for h in house_rules:
                if random.randint(1, 15) % 2 == 0:
                    room.house_rule.add(h)

        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created"))
