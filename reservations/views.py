import datetime
from django.http import Http404
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib import messages
from . import models as reservation_models
from rooms import models as room_models
from users import mixins as user_mixins
from . import models
from reviews import forms as review_forms


def create(request, room_pk, year, month, day):

    # reservation pk로 찾아서 생성 후 context로
    reservation = reservation_models.Reservation.objects.get_or_none(pk=room_pk)
    if reservation is None:
        check_in = datetime.datetime(year, month, day)
        check_out = check_in + datetime.timedelta(days=1)
        room = room_models.Room.objects.get_or_none(pk=room_pk)
        if room is not None:
            new_reservation = reservation_models.Reservation.objects.create(
                status="pending",
                check_in=check_in,
                check_out=check_out,
                guest=request.user,
                room_info=room,
            )
            return redirect(
                reverse("reservations:detail", kwargs={"pk": new_reservation.pk})
            )
        else:
            messages.error(request, "Room does not exists")
            return redirect(reverse("core:home"))
    else:
        messages.error(request, "Reservation already exists")
        return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))


class ReservationDetailView(user_mixins.LoggedInOnlyView, View):
    def get(self, request, *args, **kwargs):

        pk = kwargs.get("pk")
        reservation = reservation_models.Reservation.objects.get_or_none(pk=pk)
        if reservation is None or (
            reservation.guest != request.user
            and reservation.room_info.host != request.user
        ):
            raise Http404()
        form = review_forms.CreateReviewForm()
        return render(
            request,
            "reservations/reservation_detail.html",
            context={"reservation": reservation, "form": form},
        )


def edit_reservation(request, pk, verb):

    reservation = reservation_models.Reservation.objects.get_or_none(pk=pk)
    if reservation is None or (
        reservation.guest != request.user and reservation.room_info.host != request.user
    ):
        raise Http404()

    if verb == "cancel":
        reservation.status = models.Reservation.STATUS_CANCELED
        models.BookedDay.objects.filter(reserve=reservation).delete()
    elif verb == "confirm":
        reservation.status = models.Reservation.STATUS_CONFIRMED
    reservation.save()
    messages.success(request, "Reservation Updated")

    return redirect(reverse("reservations:detail", kwargs={"pk": pk}))
