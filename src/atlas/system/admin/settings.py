from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from system.admin.translation import UnfoldTabbedTranslationAdmin

from ..models.settings import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(UnfoldTabbedTranslationAdmin):
    """
    Admin for site settings.
    Only one record is expected (Singleton pattern).
    """

    list_display = ("__str__", "app_mode_enabled", "maintenance_mode")
    readonly_fields = ()

    fieldsets = (
        (
            _("Contact"),
            {
                "fields": (
                    "phone",
                    "email",
                    "address_street",
                    "address_locality",
                    "address_postal_code",
                    "contact_person",
                    "working_hours",
                    "default_locale",
                )
            },
        ),
        (
            _("Editorial fallback"),
            {
                "fields": ("hero_fallback_title", "hero_fallback_intro", "hero_fallback_image"),
                "classes": ("tab",),
            },
        ),
        (
            _("Geography"),
            {
                "fields": ("google_maps_link", "latitude", "longitude"),
                "classes": ("tab",),
            },
        ),
        (
            _("Social"),
            {
                "fields": (
                    "instagram_url",
                    "facebook_url",
                    "telegram_url",
                    "whatsapp_url",
                    "youtube_url",
                    "linkedin_url",
                    "tiktok_url",
                    "twitter_url",
                    "pinterest_url",
                ),
                "classes": ("tab",),
            },
        ),
        (
            _("Marketing"),
            {
                "fields": (
                    "google_analytics_id",
                    "google_tag_manager_id",
                    "facebook_pixel_id",
                    "tiktok_pixel_id",
                ),
                "classes": ("tab",),
            },
        ),
        (
            _("Technical"),
            {"fields": ("app_mode_enabled", "maintenance_mode", "head_scripts", "body_scripts")},
        ),
    )

    def has_add_permission(self, request):
        # Restrict creation when a record already exists (Singleton)
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False
