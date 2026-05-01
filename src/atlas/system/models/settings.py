from codex_django.messaging import AbstractEmailSettings, EmailSettingsSyncMixin
from codex_django.system.mixins.settings import (
    AbstractSiteSettings,
    SiteContactSettingsMixin,
    SiteGeoSettingsMixin,
    SiteMarketingSettingsMixin,
    SiteSocialSettingsMixin,
    SiteTechnicalSettingsMixin,
)
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

    @classmethod
    def load(cls) -> "SiteSettings":
        obj, _created = cls.objects.get_or_create(pk=1)
        return obj

    class Meta:
        verbose_name = _("Настройки сайта")
        verbose_name_plural = _("Настройки сайта")


class EmailSettings(AbstractEmailSettings, EmailSettingsSyncMixin):
    """Dedicated messaging/email settings singleton."""

    class Meta:
        verbose_name = _("Настройки email")
        verbose_name_plural = _("Настройки email")
