from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.contrib import messages


class LoggedOutOnlyView(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.info(self.request, "You already logged in")
        return redirect(reverse("core:home"))


class LoggedInOnlyView(LoginRequiredMixin):

    login_url = reverse_lazy("users:login")


class EmailOnlyView(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.login_method == "email"

    def handle_no_permission(self):
        messages.info(self.request, "Github and Kakao can't change password")
        return redirect(reverse("core:home"))
