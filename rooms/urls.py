from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("<int:pk>/", views.RoomView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.EditRoomView.as_view(), name="edit"),
    path("<int:pk>/photos/", views.EditPhotoView.as_view(), name="photos"),
    path("<int:pk>/photos/add", views.UploadPhotoView.as_view(), name="upload-photo"),
    path(
        "<int:room_pk>/photos/<int:photo_pk>/delete/",
        views.delete_photo,
        name="delete-photo",
    ),
    path(
        "<int:room_pk>/photos/<int:photo_pk>/edit/",
        views.UpdatePhotoView.as_view(),
        name="update-photo",
    ),
    path("search/", views.SearchView.as_view(), name="search"),
]
