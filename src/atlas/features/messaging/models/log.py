from codex_django.messaging import AbstractEmailLog


def _(message: str) -> str:
    return message


class EmailLog(AbstractEmailLog):
    class Meta:
        verbose_name = _("Email log")
        verbose_name_plural = _("Email logs")
