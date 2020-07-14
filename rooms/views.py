from django.http import Http404
from django.views.generic import ListView, DetailView, View, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.http import Http404
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django_countries import countries
from . import models, forms
from users import mixins as user_mixins

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
    paginate_by = 12
    paginate_orphans = 5
    context_object_name = "rooms"
    ordering = "created"


class RoomView(DetailView):

    model = models.Room


class SearchView(View):
    def get(self, request):
        country = request.GET.get("country")

        if country:

            form = forms.SearchForm(request.GET)

            if form.is_valid():
                country = form.cleaned_data.get("country")
                city = form.cleaned_data.get("city")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                beds = form.cleaned_data.get("beds")
                bedrooms = form.cleaned_data.get("bedrooms")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                room_type = form.cleaned_data.get("room_type")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if price is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if baths is not None:
                    filter_args["bath__gte"] = baths

                for a in amenities:
                    filter_args["amenity"] = a

                for f in facilities:
                    filter_args["facility"] = f

                if instant_book is True:
                    filter_args["instant_book"] = instant_book

                if superhost is True:
                    filter_args["host__superhost"] = superhost

                rooms = models.Room.objects.filter(**filter_args)

                return render(
                    request, "rooms/search.html", {"form": form, "rooms": rooms}
                )
        else:
            form = forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form})


class EditRoomView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.Room
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "bath",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenity",
        "facility",
        "house_rule",
    )
    template_name = "rooms/room_edit.html"
    success_message = "Room Updated"

    def get_object(self, queryset=None):

        room = super().get_object(queryset=queryset)

        if room.host.pk != self.request.user.pk:
            raise Http404()
        else:
            return room


class EditPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, DetailView):

    model = models.Room
    success_message = "Photos Updated"
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):

        room = super().get_object(queryset=queryset)

        if room.host.pk != self.request.user.pk:
            raise Http404()
        else:
            return room


def delete_photo(request, room_pk, photo_pk):

    user = request.user

    try:
        room = models.Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, "Permission denied")
        else:
            room.photos.filter(pk=photo_pk).delete()
            messages.success(request, "Deleted Photo")
    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))

    return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))

