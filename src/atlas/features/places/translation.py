from modeltranslation.translator import TranslationOptions, register

from .models import City, Country, Place, PlaceFact, PlaceImage, Region, SeasonTag


@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ("name", "intro", "seo_title", "seo_description")


@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ("name", "intro", "seo_title", "seo_description")


@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ("name", "intro", "seo_title", "seo_description")


@register(Place)
class PlaceTranslationOptions(TranslationOptions):
    fields = ("name", "intro", "long_form_story", "seasonality", "seasonality_text", "seo_title", "seo_description")


@register(PlaceFact)
class PlaceFactTranslationOptions(TranslationOptions):
    fields = ("label", "value", "note")


@register(PlaceImage)
class PlaceImageTranslationOptions(TranslationOptions):
    fields = ("caption", "alt_text")


@register(SeasonTag)
class SeasonTagTranslationOptions(TranslationOptions):
    fields = ("name",)
