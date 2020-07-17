from django.shortcuts import render


def create(request, pk):

    # reservation pk로 찾아서 생성 후 context로

    return render(request, "reservations/reservation_detail.html")
