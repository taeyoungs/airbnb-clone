from django.urls import path
from . import views

app_name = "reviews"


urlpatterns = [
    path("<int:room_pk>/create/", views.create_review, name="create"),
]
