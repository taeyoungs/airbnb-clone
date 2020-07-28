from django.db import models


class CustomModelManager(models.Manager):
    def get_or_none(self, **kwargs):

        pk = kwargs.get("pk")
        try:
            model = self.model.objects.get(pk=pk)
            return model
        except self.model.DoesNotExist:
            return None
