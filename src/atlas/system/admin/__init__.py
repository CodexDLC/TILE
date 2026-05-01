from .email_settings import EmailSettingsAdmin
from .seo import StaticPageSeoAdmin
from .settings import SiteSettingsAdmin
from .static import StaticTranslationAdmin
from .user_profile import UserProfileAdmin

__all__ = [
    "EmailSettingsAdmin",
    "SiteSettingsAdmin",
    "StaticTranslationAdmin",
    "StaticPageSeoAdmin",
    "UserProfileAdmin",
]
