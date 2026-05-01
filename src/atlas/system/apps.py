from django.apps import AppConfig
def _(message: str) -> str:
    return message


class SystemConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "system"
    label = "system"
    verbose_name = _("Система")
