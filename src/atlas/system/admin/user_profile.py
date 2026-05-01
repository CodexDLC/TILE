from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

from ..models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(ModelAdmin):
    list_display = ("id", "user", "last_name", "first_name", "phone", "source", "created_at")
    list_filter = ("source", "created_at")
    search_fields = ("user__username", "user__email", "first_name", "last_name", "phone", "notes")
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("user",)
    date_hierarchy = "created_at"
    fieldsets = (
        (
            _("Profile"),
            {
                "fields": (
                    "user",
                    "first_name",
                    "last_name",
                    "patronymic",
                    "phone",
                    "birth_date",
                    "avatar",
                )
            },
        ),
        (
            _("Acquisition"),
            {
                "fields": (
                    "source",
                    "notes",
                )
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
