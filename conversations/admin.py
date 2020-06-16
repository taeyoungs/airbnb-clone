from django.contrib import admin
from . import models


@admin.register(models.Conversation)
class ConversationAdmin(admin.ModelAdmin):

    """ Conversation Admin Definition """

    list_display = ("__str__", "count_participants")


@admin.register(models.Message)
class Message(admin.ModelAdmin):

    """ Message Admin Definition """

    list_display = ("__str__", "created")
