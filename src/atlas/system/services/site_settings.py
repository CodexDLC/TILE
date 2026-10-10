from __future__ import annotations

from typing import Any

from codex_django.cabinet.services.site_settings import SiteSettingsService as LibrarySiteSettingsService


class SiteSettingsService(LibrarySiteSettingsService):
    """TALE access policy; rendering and persistence belong to the library."""

    @classmethod
    def user_can_access(cls, user: Any) -> bool:
        return bool(user.is_authenticated and user.is_active and (user.is_staff or user.is_superuser))
