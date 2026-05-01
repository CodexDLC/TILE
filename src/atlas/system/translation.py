from modeltranslation.translator import TranslationOptions, register

from .models import SiteSettings, StaticPageSeo, StaticTranslation


@register(SiteSettings)
class SiteSettingsTranslationOptions(TranslationOptions):
    fields = (
        "contact_person",
        "working_hours",
        "hero_fallback_title",
        "hero_fallback_intro",
    )


@register(StaticPageSeo)
class StaticPageSeoTranslationOptions(TranslationOptions):
    fields = ("seo_title", "seo_description")


@register(StaticTranslation)
class StaticTranslationTranslationOptions(TranslationOptions):
    fields = ("content",)
