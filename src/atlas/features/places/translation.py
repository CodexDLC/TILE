from modeltranslation.translator import TranslationOptions, register

from .models import City, Country, Place, Region


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
