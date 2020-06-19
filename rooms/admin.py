from django.contrib import admin
from django.utils.html import mark_safe
from . import models


@admin.register(models.RoomType, models.Amenity, models.Facility, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()


class PhotoInline(admin.TabularInline):
    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin Definition """

    inlines = [
        PhotoInline,
    ]

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
        "total_average",
    )

    list_filter = ("host__superhost", "amenity", "facility", "city", "country")

    search_fields = ("=city", "^host__username")

    filter_horizontal = ("amenity", "facility", "house_rule")

    def count_amenities(self, obj):
        return obj.amenity.count()

    count_amenities.short_description = "num of amentities"

    raw_id_fields = ("host",)


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(f"<img width='50px' src='{obj.file.url}' />")

    get_thumbnail.short_description = "thumbnail"
