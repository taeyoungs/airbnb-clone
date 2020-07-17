from django.urls import path
from . import views

app_name = "reservations"

urlpatterns = [
    path("<int:pk>/create", views.create, name="create"),
]

