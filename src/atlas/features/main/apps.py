from django.apps import AppConfig
def _(message: str) -> str:
    return message


class MainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "features.main"
    verbose_name = _("Main")
