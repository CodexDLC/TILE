from typing import ClassVar

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from system.admin.translation import UnfoldTabbedTranslationAdmin, UnfoldTranslationTabularInline

from .models import City, Country, Place, PlaceFact, PlaceImage, PlaceSeasonTag, Region, SeasonTag


class PlaceFactInline(UnfoldTranslationTabularInline):
    model = PlaceFact
    extra = 0
    fields = ("order", "label", "value", "note", "icon", "is_visible")


class PlaceImageInline(UnfoldTranslationTabularInline):
    model = PlaceImage
    extra = 0
    fields = ("order", "image", "caption", "alt_text", "is_cover")


class PlaceSeasonTagInline(admin.TabularInline):
    model = PlaceSeasonTag
    extra = 0
    fields = ("order", "tag")


@admin.register(Country)
class CountryAdmin(UnfoldTabbedTranslationAdmin):
    list_display = ("name", "slug", "page")
    search_fields = ("name", "slug")
    prepopulated_fields: ClassVar[dict[str, tuple[str, ...]]] = {"slug": ("name",)}
    fieldsets = (
        (None, {"fields": ("name", "slug", "page", "hero_image", "intro")}),
        (_("SEO"), {"fields": ("seo_title", "seo_description", "seo_image")}),
    )


@admin.register(Region)
class RegionAdmin(UnfoldTabbedTranslationAdmin):
    list_display = ("name", "country", "slug", "page")
    list_filter = ("country",)
    search_fields = ("name", "slug")
    prepopulated_fields: ClassVar[dict[str, tuple[str, ...]]] = {"slug": ("name",)}
    fieldsets = (
        (None, {"fields": ("country", "name", "slug", "page", "hero_image", "intro")}),
        (_("SEO"), {"fields": ("seo_title", "seo_description", "seo_image")}),
    )


@admin.register(City)
class CityAdmin(UnfoldTabbedTranslationAdmin):
    list_display = ("name", "region", "slug", "page")
    list_filter = ("region__country", "region")
    search_fields = ("name", "slug")
    prepopulated_fields: ClassVar[dict[str, tuple[str, ...]]] = {"slug": ("name",)}
    fieldsets = (
        (None, {"fields": ("region", "name", "slug", "page", "hero_image", "intro")}),
        (_("SEO"), {"fields": ("seo_title", "seo_description", "seo_image")}),
    )


@admin.register(Place)
class PlaceAdmin(UnfoldTabbedTranslationAdmin):
    list_display = ("name", "city", "slug", "page")
    list_filter = ("city__region__country", "city__region", "city")
    search_fields = ("name", "slug", "intro", "long_form_story")
    prepopulated_fields: ClassVar[dict[str, tuple[str, ...]]] = {"slug": ("name",)}
    inlines = (PlaceFactInline, PlaceImageInline, PlaceSeasonTagInline)
    fieldsets = (
        (None, {"fields": ("city", "name", "slug", "page", "hero_image", "intro")}),
        (_("Контент"), {"fields": ("long_form_story",)}),
        (_("Сезонность"), {"fields": ("seasonality", "seasonality_text")}),
        (_("Координаты"), {"fields": ("latitude", "longitude")}),
        (_("SEO"), {"fields": ("seo_title", "seo_description", "seo_image")}),
    )


@admin.register(SeasonTag)
class SeasonTagAdmin(UnfoldTabbedTranslationAdmin):
    list_display = ("name", "slug", "color", "icon")
    search_fields = ("name", "slug")
    prepopulated_fields: ClassVar[dict[str, tuple[str, ...]]] = {"slug": ("name",)}
    fieldsets = (
        (None, {"fields": ("name", "slug", "color", "icon")}),
    )
