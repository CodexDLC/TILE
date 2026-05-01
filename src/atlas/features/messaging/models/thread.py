import secrets
from typing import ClassVar

from codex_django.messaging import AbstractThread
from django.db import models


def _(message: str) -> str:
    return message


class Thread(AbstractThread):
    class Status(models.TextChoices):
        OPEN = "open", _("Open")
        PROCESSED = "processed", _("Processed")
        SPAM = "spam", _("Spam")

    topic = models.CharField(max_length=30, blank=True, db_index=True)
    source = models.CharField(max_length=20, blank=True, db_index=True)
    channel = models.CharField(max_length=20, default="email", db_index=True)
    sender_name = models.CharField(max_length=255, blank=True)
    sender_email = models.EmailField(blank=True)
    sender_phone = models.CharField(max_length=50, blank=True)
    is_read = models.BooleanField(default=False, db_index=True)
    is_archived = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering: ClassVar[list[str]] = ["-last_activity_at"]
        verbose_name = _("Thread")
        verbose_name_plural = _("Threads")

    def save(self, *args, **kwargs):
        if not self.thread_key:
            self.thread_key = secrets.token_urlsafe(32)
        super().save(*args, **kwargs)
