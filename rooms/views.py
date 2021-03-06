from django.http import Http404
from django.views.generic import ListView, DetailView, View, UpdateView, FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
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

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        paginator = context["paginator"]
        page_numbers_range = 5  # Display only 5 page numbers
        max_index = len(paginator.page_range)

        page = self.request.GET.get("page")
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        context["has_next"] = False
        if end_index + 1 <= max_index:
            context["has_next"] = True
            context["next"] = end_index + 1

        context["has_previous"] = False
        if start_index != 0:
            context["has_previous"] = True
            context["previous"] = start_index

        page_range = paginator.page_range[start_index:end_index]
        context["page_range"] = page_range
        return context


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


class EditPhotoView(user_mixins.LoggedInOnlyView, DetailView):

    model = models.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):

        room = super().get_object(queryset=queryset)

        if room.host.pk != self.request.user.pk:
            raise Http404()
        else:
            return room


@login_required
def delete_photo(request, room_pk, photo_pk):

    user = request.user

    try:
        room = models.Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, "Permission denied")
        else:
            room.photos.filter(pk=photo_pk).delete()
            messages.success(request, "Photo Deleted")
    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))

    return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))


class UpdatePhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.Photo
    fields = ("caption",)
    success_message = "Photo Updated"
    pk_url_kwarg = "photo_pk"
    template_name = "rooms/photo_edit.html"

    def get_success_url(self):

        room_pk = self.kwargs.get("room_pk")

        return reverse("rooms:photos", kwargs={"pk": room_pk})


class UploadPhotoView(user_mixins.LoggedInOnlyView, FormView):

    form_class = forms.CreatePhotoForm
    template_name = "rooms/photo_upload.html"

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(pk)
        messages.success(request, "Photo Uploaded")

        return redirect(reverse("rooms:photos", kwargs={"pk": pk}))


class CreateRoomView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, FormView):

    form_class = forms.CreateRoomForm
    template_name = "rooms/room_create.html"
    success_message = "Room Created"

    def form_valid(self, form):
        user = self.request.user
        room = form.save()
        room.host = user
        room.save()
        form.save_m2m()

        return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))


@login_required
def delete_room(request, pk):

    try:
        room = models.Room.objects.get(pk=pk)
        if room.host.pk != request.user.pk:
            messages.error(request, "Permission denied")
        else:
            models.Room.objects.get(pk=pk).delete()
    except models.Room.DoesNotExist:
        messages.error(request, "Room does not exist")
        return redirect(reverse("core:home"))

    messages.success(request, "Room deleted")
    return redirect(reverse("core:home"))

