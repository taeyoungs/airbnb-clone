from django.views.generic import ListView
from django.urls import reverse
from django.shortcuts import render, redirect
from . import models

"""
def all_rooms(request):

    # pagination (without django func)
    
    page = int(request.GET.get("page", 1))
    page_size = 10
    limit = page_size * page
    offset = limit - page_size
    all_rooms = models.Room.objects.all()[offset:limit]
    page_count = ceil(models.Room.objects.count() / page_size)

    return render(
        request,
        "rooms/home.html",
        context={
            "room_list": all_rooms,
            "page": page,
            "page_count": page_count,
            "page_range": range(1, page_count+1),
        },
    ) 
    

    # pagination (using django paginator)
    page = int(request.GET.get("page", 1))
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10, orphans=5)

    try:
        rooms = paginator.page(page)
        return render(request, "rooms/home.html", {"page": rooms})
    except EmptyPage:
        return redirect("/")
"""


class HomeView(ListView):

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    context_object_name = "rooms"


def detail(request, pk):

    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", {"room": room})
    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))
