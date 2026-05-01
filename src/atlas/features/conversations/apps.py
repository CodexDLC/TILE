from django.apps import AppConfig
def _(message: str) -> str:
    return message


class ConversationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "features.conversations"
    verbose_name = _("Conversations")
