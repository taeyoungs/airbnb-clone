from django.db import models
from core import models as core_models


class Conversation(core_models.TimeStampedModel):

    participants = models.ManyToManyField("users.User")

    def __str__(self):
        return str(self.created)


class Message(core_models.TimeStampedModel):

    msg = models.TextField()
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    chat_room = models.ForeignKey("Conversation", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.msg} - {self.user}"
