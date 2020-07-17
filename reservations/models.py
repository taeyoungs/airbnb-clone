from datetime import timedelta
from django.db import models
from django.utils import timezone
from core import models as core_models


class BookedDay(core_models.TimeStampedModel):
    day = models.DateField()
    reserve = models.ForeignKey("Reservation", on_delete=models.CASCADE)


class Reservation(core_models.TimeStampedModel):

    """ Reservation Model Definition """

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELED, "Canceled"),
    )

    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    check_in = models.DateField()
    check_out = models.DateField()
    guest = models.ForeignKey(
        "users.User", related_name="reservations", on_delete=models.CASCADE
    )
    room_info = models.ForeignKey(
        "rooms.Room", related_name="reservations", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.room_info.name

    def in_progress(self):
        now = timezone.now().date()
        return now >= self.check_in and now <= self.check_out

    in_progress.boolean = True

    def is_finished(self):
        now = timezone.now().date()
        return now > self.check_out

    is_finished.boolean = True

    def save(self, *args, **kwargs):
        start = self.check_in
        end = self.check_out
        diff = end - start
        existing_booked_days = BookedDay.objects.filter(
            day__range=(start, end)
        ).exists()
        if not existing_booked_days:
            super(Reservation, self).save(*args, **kwargs)
            for d in range(0, diff.days + 1):
                day = self.check_in + timedelta(days=d)
                BookedDay.objects.create(day=day, reserve=self)
            return
        return super(Reservation, self).save(*args, **kwargs)
