from django.contrib.auth.mixins import UserPassesTestMixin


class LoggedOutOnlyView(UserPassesTestMixin, View):
    def test_func(self):
        return True
