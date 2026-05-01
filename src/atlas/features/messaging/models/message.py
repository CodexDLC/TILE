from typing import ClassVar

from codex_django.messaging import AbstractMessage
from django.db import models


def _(message: str) -> str:
    return message


class Message(AbstractMessage):
    class Direction(models.TextChoices):
        INBOUND = "inbound", _("Inbound")
        OUTBOUND = "outbound", _("Outbound")

    thread = models.ForeignKey(
        "messaging.Thread",
        on_delete=models.CASCADE,
        related_name="messages",
    )

    class Meta:
        ordering: ClassVar[list[str]] = ["created_at"]
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
