from django.db import models
from django.contrib.auth.models import UserManager


class CustomModelManager(models.Manager):
    def get_or_none(self, **kwargs):

        pk = kwargs.get("pk")
        try:
            model = self.model.objects.get(pk=pk)
            return model
        except self.model.DoesNotExist:
            return None


class CustomUserManager(CustomModelManager, UserManager):
    pass
