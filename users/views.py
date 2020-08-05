import os
from django.utils import translation
from django.http import HttpResponse
from django.views.generic import FormView, DetailView, UpdateView, TemplateView
from django.contrib.auth.views import PasswordChangeView
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
import requests
from . import forms, models, mixins


class LoginView(mixins.LoggedOutOnlyView, FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f"Welcome back, {user.first_name}")

        return super().form_valid(form)

    """
    def post(self, request):

        form = forms.LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("core:home"))

        return render(request, "users/login.html", {"form": form})
    """

    def get_success_url(self):
        next_location = self.request.GET.get("next")
        if next_location is not None:
            return next_location
        else:
            return reverse("core:home")


def log_out(request):
    logout(request)
    messages.info(request, f"Bye, See you later")
    return redirect(reverse("core:home"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):

    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):

        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()

        return super().form_valid(form)


def complete_verification(request, secret):
    try:
        user = models.User.objects.get(email_secret=secret)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # to do success error messages
        return redirect(reverse("core:home"))
    except models.User.DoesNotExist:
        # to do fail error messages
        pass


def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8001/users/login/github/callback/"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        # Github에서 code가 오지 않았을 경우 raise Error
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        code = request.GET.get("code", None)
        if code is not None:
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json",},
            )
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:
                raise GithubException("Token doesn't exist")
            token = token_json.get("access_token")
            if token is not None:
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {token}",
                        "Accept": "application/json",
                    },
                )
                profile_json = profile_request.json()
                name = profile_json.get("name")
                if name is not None:
                    email = profile_json.get("email")
                    bio = profile_json.get("bio")
                    profile_image = profile_json.get("avatar_url")
                    if bio is None:
                        bio = ""
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException(
                                f"Please login with {user.login_method}"
                            )
                    except models.User.DoesNotExist:
                        # create new user
                        user = models.User.objects.create(
                            email=email,
                            username=email,
                            first_name=name,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        user.set_unusable_password()
                        user.save()
                        photo_request = requests.get(profile_image)
                        if photo_request is not None:
                            user.avatar.save(
                                f"{name}-avatar", ContentFile(photo_request.content)
                            )
                    login(request, user)
                    messages.success(request, f"Welcome back, {user.first_name}")
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException("Profile doesn't exist")
            else:
                raise GithubException("Token doesn't exist")
        else:
            raise GithubException("Code doesn't exist")
    except GithubException as e:
        print(e)
        messages.error(request, e)
        return redirect(reverse("users:login"))


def kakao_login(request):
    client_id = os.environ.get("KAKAO_ID")
    redirect_uri = "http://127.0.0.1:8001/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    code = request.GET.get("code", None)
    client_id = os.environ.get("KAKAO_ID")
    redirect_uri = "http://127.0.0.1:8001/users/login/kakao/callback"
    try:
        if code is not None:
            token_request = requests.post(
                f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
            )
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:
                raise KakaoException("Token doesn't exist")
            token = token_json.get("access_token", None)
            if token is not None:
                profile_request = requests.get(
                    "https://kapi.kakao.com/v2/user/me",
                    headers={"Authorization": f"Bearer {token}"},
                )
                profile_json = profile_request.json()
                properties = profile_json.get("kakao_account").get("profile")
                if properties is not None:
                    email = profile_json.get("kakao_account").get("email")
                    nickname = properties.get("nickname")
                    profile_image = properties.get("profile_image_url")
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_KAKAO:
                            raise KakaoException(
                                f"Please login with {user.login_method}"
                            )
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            first_name=nickname,
                            email=email,
                            username=email,
                            login_method=models.User.LOGIN_KAKAO,
                            email_verified=True,
                        )
                        user.set_unusable_password()
                        user.save()
                        photo_request = requests.get(profile_image)
                        if photo_request is not None:
                            user.avatar.save(
                                f"{nickname}-avatar", ContentFile(photo_request.content)
                            )
                    login(request, user)
                    messages.success(request, f"Welcome back, {user.first_name}")
                    return redirect(reverse("core:home"))
                else:
                    raise KakaoException("Profile doesn't exist")
            else:
                raise KakaoException("Token doesn't exist")
        else:
            raise KakaoException("Code doesn't exist")
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):

    model = models.User
    context_object_name = "user_obj"


class UpdateProfileView(
    mixins.LoggedInOnlyView, mixins.EmailOnlyView, SuccessMessageMixin, UpdateView
):

    model = models.User
    fields = [
        "first_name",
        "last_name",
        "gender",
        "bio",
        "birthdate",
        "language",
        "currency",
    ]
    template_name = "users/update_profile.html"
    success_message = "Profile Updated"

    def get_object(self, queryset=None):
        # 로그인한 유저 정보
        return self.request.user

    def get_form(self, form_class=None):

        form = super().get_form(form_class=form_class)

        form.fields["first_name"].widget.attrs = {"placeholder": "First name"}
        form.fields["last_name"].widget.attrs = {"placeholder": "Last name"}
        form.fields["bio"].widget.attrs = {"placeholder": "bio"}
        form.fields["birthdate"].widget.attrs = {"placeholder": "Birthdate"}

        return form


class UpdatePasswordView(
    mixins.LoggedInOnlyView,
    mixins.EmailOnlyView,
    SuccessMessageMixin,
    PasswordChangeView,
):

    template_name = "users/update_password.html"
    success_message = "Password Updated"

    def get_form(self, form_class=None):

        form = super().get_form(form_class=form_class)

        form.fields["old_password"].widget.attrs = {"placeholder": "Current password"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "New password"}
        form.fields["new_password2"].widget.attrs = {
            "placeholder": "Confirm new password"
        }

        return form


def switch_hosting(request):
    # print(request.session["is_hosting"])
    try:
        del request.session["is_hosting"]
    except KeyError:
        request.session["is_hosting"] = True
    return redirect(reverse("core:home"))


def switch_lang(request):

    lang = request.GET.get("lang", None)
    print(lang, request.session[translation.LANGUAGE_SESSION_KEY])
    if lang is not None:
        del request.session[translation.LANGUAGE_SESSION_KEY]
        translation.activate(lang)
        request.session[translation.LANGUAGE_SESSION_KEY] = lang

    return HttpResponse(status=200)


class UserReservationListView(TemplateView):

    template_name = "users/user_reservation_list.html"
