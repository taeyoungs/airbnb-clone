import calendar
from django.utils import timezone


class Day:
    def __init__(self, year, month, day, past):
        self.day = day
        self.past = past
        self.year = year
        self.month = month


class Calendar(calendar.Calendar):
    def __init__(self, year, month):
        super().__init__(firstweekday=6)
        self.year = year
        self.month = month
        self.day_names = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        self.months = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "October",
            "November",
            "Setember",
        ]

    def get_days(self):
        weeks = self.monthdays2calendar(self.year, self.month)
        now = timezone.now()
        days = []
        for week in weeks:
            for d, m in week:
                if now.month == self.month:
                    if d < now.day:
                        days.append(Day(self.year, self.month, d, True))
                    else:
                        days.append(Day(self.year, self.month, d, False))
                else:
                    days.append(Day(self.year, self.month, d, False))
        return days

    def get_month(self):
        return self.months[self.month - 1]
