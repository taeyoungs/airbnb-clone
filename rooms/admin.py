from django.contrib import admin
from . import models


@admin.register(models.Room)
class CustomRoomAdmin(admin.ModelAdmin):

    """ Custom Room Admin """

    pass
