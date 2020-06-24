from django.views.generic import ListView
from django.urls import reverse
from django.http import Http404
from django.shortcuts import render, redirect
from django_countries import countries
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
        raise Http404()


def search(request):
    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    s_country = request.GET.get("country", "KR")
    s_room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    beds = int(request.GET.get("beds", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    baths = int(request.GET.get("baths", 0))
    s_amenities = list(map(int, request.GET.getlist("amenities")))
    s_facilities = list(map(int, request.GET.getlist("facilities")))

    form = {
        "city": city,
        "s_country": s_country,
        "s_room_type": s_room_type,
        "price": price,
        "guests": guests,
        "beds": beds,
        "bedrooms": bedrooms,
        "baths": baths,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
    }

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    filter_args = {}

    if city != "Anywhere":
        filter_args["city__startswith"] = city

    filter_args["country"] = s_country

    if s_room_type != 0:
        filter_args["room_type"] = s_room_type

    if price != 0:
        filter_args["price__lte"] = price

    if beds != 0:
        filter_args["beds__gte"] = beds

    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms

    if guests != 0:
        filter_args["guests__gte"] = guests

    if baths != 0:
        filter_args["baths__gte"] = baths

    if len(s_amenities) > 0:
        for a in s_amenities:
            filter_args["amenity__pk"] = a

    if len(s_facilities) > 0:
        for f in s_facilities:
            filter_args["facility__pk"] = f

    rooms = models.Room.objects.filter(**filter_args)

    return render(request, "rooms/search.html", {**form, **choices, "rooms": rooms})
