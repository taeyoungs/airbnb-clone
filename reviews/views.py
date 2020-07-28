from django.shortcuts import redirect, reverse
from . import forms
from rooms import models as room_models


def create_review(request, room_pk):
    if request.method == "POST":
        form = forms.CreateReviewForm(request.POST)
        room = room_models.Room.objects.get_or_none(pk=room_pk)
        if room is not None:
            if form.is_valid():
                review = form.save()
                review.room_info = room
                review.user = request.user
                review.save()
        else:
            return redirect(reverse("core:home"))

    return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))
