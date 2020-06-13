from django.db import models


class TimeStampedModel(models.Model):

    """ Time Stamp Model """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class meta:
        abstract = True
