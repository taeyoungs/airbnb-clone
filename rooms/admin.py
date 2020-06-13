from django.contrib import admin
from . import models


@admin.register(models.RoomType, models.Amenity, models.Facility, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin Definition """

    fieldsets = (
        ("Basic Info", {"fields": ("name", "country", "city", "price",)}),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")}),
        ("Spaces", {"fields": ("guests", "beds", "bedrooms", "bath")}),
        (
            "More About the Space",
            {
                "classes": ("collapse",),
                "fields": ("room_type", "amenity", "facility", "house_rule"),
            },
        ),
        ("Other", {"fields": ("host",)}),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "bath",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
    )

    list_filter = ("host__superhost", "amenity", "facility", "city", "country")

    search_fields = ("=city", "^host__username")

    filter_horizontal = ("amenity", "facility", "house_rule")

    def count_amenities(self, obj):
        return obj.amenity.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    pass
