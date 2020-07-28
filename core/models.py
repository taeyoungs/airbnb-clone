from django.db import models
from . import managers


class TimeStampedModel(models.Model):

    """ Time Stamp Model """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = managers.CustomModelManager()

    class meta:
        abstract = True
