from django.db import models
from core import models as core_models


class Conversation(core_models.TimeStampedModel):

    participants = models.ManyToManyField("users.User", related_name="conversations")

    def __str__(self):
        members = self.participants.all()
        usernames = []
        for member in members:
            usernames.append(member.username)
        return ", ".join(usernames)

    def count_participants(self):
        return self.participants.count()

    count_participants.short_description = "number of participants"


class Message(core_models.TimeStampedModel):

    msg = models.TextField()
    user = models.ForeignKey(
        "users.User", related_name="messages", on_delete=models.CASCADE
    )
    chat_room = models.ForeignKey(
        "Conversation", related_name="messages", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user} says: {self.msg}"
