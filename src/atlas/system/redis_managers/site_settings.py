from codex_django.core.redis.managers.settings import DjangoSiteSettingsManager


class AtlasSiteSettingsManager(DjangoSiteSettingsManager):
    CACHE_KEY = "atlas:site_settings"


def get_atlas_site_settings_manager() -> AtlasSiteSettingsManager:
    return AtlasSiteSettingsManager()
