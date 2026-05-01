from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

from ..models import EmailSettings


@admin.register(EmailSettings)
class EmailSettingsAdmin(ModelAdmin):
    list_display = ("email_from", "email_sender_name", "site_base_url")
    search_fields = ("email_from", "email_sender_name", "email_reply_to", "site_base_url")

    fieldsets = (
        (
            _("Email identity"),
            {
                "fields": (
                    "email_from",
                    "email_sender_name",
                    "email_reply_to",
                )
            },
        ),
        (
            _("Messaging URLs"),
            {
                "fields": (
                    "site_base_url",
                    "logo_url",
                    "url_path_confirm",
                    "url_path_cancel",
                    "url_path_reschedule",
                    "url_path_contact_form",
                )
            },
        ),
    )

    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False
