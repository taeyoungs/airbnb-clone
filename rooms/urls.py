from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("<int:pk>", views.RoomView.as_view(), name="detail"),
    path("search/", views.SearchView.as_view(), name="search"),
]
