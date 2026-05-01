from typing import ClassVar

from codex_django.messaging import AbstractMessageReply
from django.db import models


def _(message: str) -> str:
    return message


class MessageReply(AbstractMessageReply):
    message = models.ForeignKey(
        "messaging.Message",
        on_delete=models.CASCADE,
        related_name="replies",
        verbose_name=_("message"),
    )
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering: ClassVar[list[str]] = ["sent_at"]
        verbose_name = _("Reply")
        verbose_name_plural = _("Replies")
