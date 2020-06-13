from django.contrib import admin
from . import models


@admin.register(models.Conversation)
class ConversationAdmin(admin.ModelAdmin):

    """ Conversation Admin Definition """

    pass


@admin.register(models.Message)
class Message(admin.ModelAdmin):

    """ Message Admin Definition """

    pass
