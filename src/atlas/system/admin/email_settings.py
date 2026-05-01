from django.contrib import admin

from ..models import EmailSettings


def _(message: str) -> str:
    return message


@admin.register(EmailSettings)
class EmailSettingsAdmin(admin.ModelAdmin):
    list_display = ("email_from", "email_sender_name", "site_base_url")

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
