from django.http import Http404
from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView
from rooms import models as room_models
from . import models


def toggle_fav(request, room_pk, action):
    if room_pk is not None and action is not None:
        room = room_models.Room.objects.get_or_none(pk=room_pk)
        if room is not None:
            the_list, _ = models.List.objects.get_or_create(
                name="My Favorites", user=request.user
            )
            if action == "add":
                the_list.room.add(room)
            elif action == "remove":
                the_list.room.remove(room)
            return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))
        else:
            return Http404()


class UserFavsDetail(TemplateView):

    template_name = "lists/list_detail.html"
