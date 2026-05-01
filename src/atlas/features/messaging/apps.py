from django.apps import AppConfig


def _(message: str) -> str:
    return message


class MessagingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "features.messaging"
    label = "messaging"
    verbose_name = _("Messaging")
