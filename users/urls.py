from django.urls import path
from . import views

app_name = "users"


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("login/github/", views.github_login, name="github-login"),
    path("login/github/callback/", views.github_callback, name="github-callback"),
    path("login/kakao/", views.kakao_login, name="kakao-login"),
    path("login/kakao/callback/", views.kakao_callback, name="kakao-callback"),
    path("logout/", views.log_out, name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path(
        "verify/<str:secret>/",
        views.complete_verification,
        name="complete_verification",
    ),
    path("<int:pk>/", views.UserProfileView.as_view(), name="profile"),
    path("update-profile/", views.UpdateProfileView.as_view(), name="update-profile"),
    path(
        "update-password/", views.UpdatePasswordView.as_view(), name="update-password"
    ),
    path("is-hosting/", views.switch_hosting, name="is-hosting"),
    path("switch-lang/", views.switch_lang, name="switch-lang"),
    path("reservations/", views.UserReservationListView.as_view(), name="reservations"),
    path("sentry-debug/", trigger_error),
]
