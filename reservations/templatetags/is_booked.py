import datetime
from django import template
from reservations import models

register = template.Library()


@register.simple_tag
def is_booked(room, d):

    if d.day == 0:
        return

    try:
        date = datetime.datetime(year=d.year, month=d.month, day=d.day)
        models.BookedDay.objects.get(day=date, reserve__room_info=room)
        return True
    except models.BookedDay.DoesNotExist:
        return False
