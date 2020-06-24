from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("<int:pk>", views.detail, name="detail"),
    path("search/", views.search, name="search"),
]
