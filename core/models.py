from django.db import models


class TimeStampedModel(models.Model):

    """ Time Stamp Model """

    created = models.DateTimeField()
    updated = models.DateTimeField()

    class meta:
        abstract = True
