"""Transitional static public-site app.

Do not add new public pages here. Dynamic public pages belong in
features.content, and contact/legal pages belong in features.contacts.
"""

from django.apps import AppConfig


def _(message: str) -> str:
    return message


class MainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "features.main"
    verbose_name = _("Main (transitional)")
