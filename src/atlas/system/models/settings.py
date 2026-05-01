from codex_django.messaging import AbstractEmailSettings, EmailSettingsSyncMixin
from codex_django.system.mixins.settings import (
    AbstractSiteSettings,
    SiteContactSettingsMixin,
    SiteGeoSettingsMixin,
    SiteMarketingSettingsMixin,
    SiteSocialSettingsMixin,
    SiteTechnicalSettingsMixin,
)
from django.db import models

from system.redis_managers import AtlasSiteSettingsManager


def _(message: str) -> str:
    return message


class SiteSettings(
    AbstractSiteSettings,
    SiteContactSettingsMixin,
    SiteGeoSettingsMixin,
    SiteSocialSettingsMixin,
    SiteMarketingSettingsMixin,
    SiteTechnicalSettingsMixin,
):
    """
    Global site settings.
    Automatically synchronized with Redis.
    """

    default_locale = models.CharField(max_length=8, default="en")
    hero_fallback_title = models.CharField(max_length=255, blank=True)
    hero_fallback_intro = models.TextField(blank=True)
    hero_fallback_image = models.ImageField(upload_to="settings/hero/", blank=True, null=True)

    redis_manager_class = AtlasSiteSettingsManager

    @classmethod
    def load(cls) -> "SiteSettings":
        obj, _created = cls.objects.get_or_create(pk=1)
        return obj

    def to_dict(self) -> dict[str, object]:
        data = super().to_dict()
        image = self.hero_fallback_image
        data["hero_fallback_image"] = image.url if image else None
        return data

    class Meta:
        verbose_name = _("Настройки сайта")
        verbose_name_plural = _("Настройки сайта")


class EmailSettings(AbstractEmailSettings, EmailSettingsSyncMixin):
    """Dedicated messaging/email settings singleton."""

    class Meta:
        verbose_name = _("Настройки email")
        verbose_name_plural = _("Настройки email")
