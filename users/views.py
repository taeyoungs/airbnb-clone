import os
from django.views.generic import FormView
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
import requests
from . import forms, models


class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)

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


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):

    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    initial = {
        "first_name": "Taeyoung",
        "last_name": "Jang",
    }

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
                raise GithubException()
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
                print(profile_json)
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
                            raise GithubException()
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
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException()
            else:
                raise GithubException()
        else:
            raise GithubException()
    except GithubException:
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
                raise KakaoException()
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
                            raise KakaoException()
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
                    return redirect(reverse("core:home"))
                else:
                    raise KakaoException()
            else:
                raise KakaoException()
        else:
            raise KakaoException()
    except KakaoException:
        return redirect(reverse("users:login"))
