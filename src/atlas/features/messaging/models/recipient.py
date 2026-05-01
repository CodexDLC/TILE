from codex_django.messaging import AbstractSystemRecipient
from django.db import models


def _(message: str) -> str:
    return message


class SystemRecipient(AbstractSystemRecipient):
    locale = models.CharField(max_length=8, default="de")
    unsubscribe_token = models.CharField(max_length=128, blank=True)

    class Meta:
        verbose_name = _("Recipient")
        verbose_name_plural = _("Recipients")
