from django.urls import path
from . import views

app_name = "lists"

urlpatterns = [
    path("favs/", views.UserFavsDetail.as_view(), name="detail"),
    path("<int:room_pk>/<str:action>/", views.toggle_fav, name="toggle"),
]
