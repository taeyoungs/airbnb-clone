from django.db import models
from django_countries.fields import CountryField
from django.urls import reverse
from django.utils import timezone
from core import models as core_models
from users import models as users_models
from cal import Calendar


class AbstractItem(models.Model):

    """ AbstractItem Model Definition """

    name = models.CharField(max_length=80)

    class meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    """ RoomType Model Definition """

    class Meta:
        verbose_name = "Room Type"


class Amenity(AbstractItem):

    """ Amenity Model Definition """

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):

    """ Facility Model Definition """

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):

    """ HouseRule Model Definition """

    class Meta:
        verbose_name = "House Rule"


class Photo(models.Model):

    """ Photo Model Definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="rooms_photo")
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """ Room Model Definition """

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    bath = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        users_models.User, related_name="rooms", on_delete=models.CASCADE
    )
    room_type = models.ForeignKey(
        RoomType, related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    amenity = models.ManyToManyField(Amenity, related_name="rooms", blank=True)
    facility = models.ManyToManyField(Facility, related_name="rooms", blank=True)
    house_rule = models.ManyToManyField(HouseRule, related_name="rooms", blank=True)

    def __str__(self):
        return self.name

    def total_average(self):
        reviews = self.reviews.all()
        ratings = 0
        for review in reviews:
            ratings += review.review_average()
        if ratings == 0:
            return 0
        else:
            return round(ratings / len(reviews), 2)

    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super(Room, self).save(*args, **kwargs)  # Call the real save() method

    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def first_photo(self):
        try:
            (photo,) = self.photos.all()[:1]
            return photo.file.url
        except ValueError:
            return None

    def get_four_photos(self):
        photos = self.photos.all()[1:5]
        return photos

    def get_calendar(self):
        now = timezone.now()
        this_month = Calendar(now.year, now.month)
        next_year = now.year
        next_month = now.month + 1
        if now.month == 12:
            next_year += 1
            next_month = 1

        next_month = Calendar(next_year, next_month)
        return [this_month, next_month]
