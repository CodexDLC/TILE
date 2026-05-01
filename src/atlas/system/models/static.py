from codex_django.system.mixins import AbstractStaticTranslation
def _(message: str) -> str:
    return message


class StaticTranslation(AbstractStaticTranslation):
    """
    Concrete model for static page content/translations.
    Used by context_processor to provide content in templates.
    """

    class Meta(AbstractStaticTranslation.Meta):
        verbose_name = _("Статический перевод")
        verbose_name_plural = _("Статические переводы")
