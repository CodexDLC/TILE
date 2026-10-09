from __future__ import annotations

import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class ContentSmartDraft(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", _("Pending")
        RUNNING = "running", _("Running")
        READY = "ready", _("Ready")
        FAILED = "failed", _("Failed")
        STALE = "stale", _("Stale")
        PUBLISHED = "published", _("Published")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resource_key = models.CharField(max_length=128, db_index=True)
    target_model = models.CharField(max_length=128)
    target_object_id = models.CharField(max_length=64, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="content_smart_drafts",
    )
    base_language = models.CharField(max_length=16)
    target_languages = models.JSONField(default=list, blank=True)
    source_payload = models.JSONField(default=dict, blank=True)
    result_payload = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.PENDING, db_index=True)
    error = models.TextField(blank=True)
    arq_job_id = models.CharField(max_length=128, blank=True)
    published_object_id = models.CharField(max_length=64, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = _("Content smart draft")
        verbose_name_plural = _("Content smart drafts")
        ordering = ["-created_at"]  # noqa: RUF012

    def __str__(self) -> str:
        return f"{self.resource_key}:{self.pk}"

    def mark_published(self, obj: models.Model) -> None:
        self.status = self.Status.PUBLISHED
        self.published_object_id = str(obj.pk)
        self.published_at = timezone.now()
        self.save(update_fields=["status", "published_object_id", "published_at", "updated_at"])


class ContentSmartDraftEvent(models.Model):
    draft = models.ForeignKey(ContentSmartDraft, on_delete=models.CASCADE, related_name="events")
    status = models.CharField(max_length=32)
    message = models.TextField(blank=True)
    payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Content smart draft event")
        verbose_name_plural = _("Content smart draft events")
        ordering = ["created_at"]  # noqa: RUF012

    def __str__(self) -> str:
        return f"{self.draft_id}:{self.status}"
