from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from codex_django.messaging.cabinet import (
    CampaignComposerState,
    CampaignDetailState,
    CampaignListState,
    CampaignRowState,
    CampaignStatusSummaryState,
    DeliveryLogRowState,
    DeliveryLogState,
    MailboxActionState,
    MailboxDetailState,
    MailboxState,
    MailboxThreadState,
    MessageState,
    MessagingActionResult,
    MessagingBridge,
    MessagingSettingsSection,
    MessagingSettingsState,
    RecipientListState,
    RecipientRowState,
    ReplyComposerState,
    build_default_mailbox_folders,
)
from django.db.models import Count, Q
from django.urls import reverse
from django.utils import timezone
from system.models import EmailSettings

from .models import Campaign, EmailLog, SystemRecipient, Thread
from .selectors import get_thread_or_404
from .services.workflow import (
    archive_thread,
    create_reply,
    mark_thread_processed,
    mark_thread_read,
    mark_thread_spam,
)


def _display_datetime(value: Any) -> str:
    if not value:
        return ""
    if timezone.is_aware(value):
        value = timezone.localtime(value)
    return value.strftime("%Y-%m-%d %H:%M")


class AtlasMessagingBridge(MessagingBridge):
    def get_mailbox_state(
        self,
        *,
        user: Any,
        folder: str = "inbox",
        thread_id: str | None = None,
        filters: Mapping[str, Any] | None = None,
    ) -> MailboxState:
        filters = filters or {}
        search_query = str(filters.get("q") or "").strip()
        qs = Thread.objects.filter(is_archived=False).order_by("-last_activity_at")
        if folder == "unread":
            qs = qs.filter(is_read=False)
        elif folder == "processed":
            qs = qs.filter(status=Thread.Status.PROCESSED)
        elif folder == "spam":
            qs = qs.filter(status=Thread.Status.SPAM)
        elif folder == "archived":
            qs = Thread.objects.filter(is_archived=True).order_by("-last_activity_at")
        elif folder == "inbox":
            qs = qs.exclude(status=Thread.Status.SPAM)
        if search_query:
            qs = qs.filter(
                Q(subject__icontains=search_query)
                | Q(sender_name__icontains=search_query)
                | Q(sender_email__icontains=search_query)
                | Q(messages__body__icontains=search_query)
            ).distinct()

        threads = [self._thread_state(thread) for thread in qs[:100]]
        selected = None
        if thread_id:
            thread = get_thread_or_404(int(thread_id))
            selected = self._detail_state(thread)

        return MailboxState(
            title="Mailbox",
            folders=build_default_mailbox_folders(base_url=reverse("cabinet:messaging_inbox"), active_folder=folder),
            threads=threads,
            selected=selected,
            search_query=search_query,
            active_folder=folder,
        )

    def get_campaign_list_state(
        self,
        *,
        user: Any,
        status: str = "all",
        filters: Mapping[str, Any] | None = None,
    ) -> CampaignListState:
        filters = filters or {}
        search_query = str(filters.get("q") or "").strip()
        qs = Campaign.objects.annotate(
            recipient_total=Count("recipients"),
            sent_total=Count("recipients", filter=Q(recipients__status="sent")),
            failed_total=Count("recipients", filter=Q(recipients__status="failed")),
        ).order_by("-updated_at")
        if status != "all":
            qs = qs.filter(status=status)
        if search_query:
            qs = qs.filter(
                Q(subject__icontains=search_query)
                | Q(body_text__icontains=search_query)
                | Q(template_key__icontains=search_query)
                | Q(locale__icontains=search_query)
            )
        return CampaignListState(
            create_url=reverse("admin:messaging_campaign_add"),
            status_filters=self._campaign_status_filters(active=status),
            rows=[
                CampaignRowState(
                    id=str(campaign.pk),
                    url=reverse("admin:messaging_campaign_change", args=[campaign.pk]),
                    subject=campaign.subject,
                    status=campaign.status,
                    status_label=campaign.status.title(),
                    locale=campaign.locale,
                    recipient_count=campaign.recipient_total,
                    sent_count=campaign.sent_total,
                    failed_count=campaign.failed_total,
                    scheduled_at=_display_datetime(campaign.send_at),
                    sent_at=_display_datetime(campaign.sent_at),
                    updated_at=_display_datetime(campaign.updated_at),
                )
                for campaign in qs[:100]
            ],
        )

    def get_campaign_detail_state(self, *, user: Any, campaign_id: str) -> CampaignDetailState:
        campaign = Campaign.objects.get(pk=campaign_id)
        row = CampaignRowState(
            id=str(campaign.pk),
            url=reverse("admin:messaging_campaign_change", args=[campaign.pk]),
            subject=campaign.subject,
            status=campaign.status,
            status_label=campaign.status.title(),
            locale=campaign.locale,
            sent_at=_display_datetime(campaign.sent_at),
            updated_at=_display_datetime(campaign.updated_at),
        )
        return CampaignDetailState(campaign=row, body_preview=campaign.body_text)

    def get_campaign_composer_state(self, *, user: Any, campaign_id: str | None = None) -> CampaignComposerState:
        raise NotImplementedError("Atlas edits campaigns through Django admin for now.")

    def get_recipient_list_state(
        self,
        *,
        user: Any,
        filters: Mapping[str, Any] | None = None,
    ) -> RecipientListState:
        filters = filters or {}
        search_query = str(filters.get("q") or "").strip()
        qs = SystemRecipient.objects.order_by("email")
        if search_query:
            qs = qs.filter(
                Q(email__icontains=search_query)
                | Q(name__icontains=search_query)
                | Q(kind__icontains=search_query)
                | Q(locale__icontains=search_query)
                | Q(note__icontains=search_query)
            )
        rows = [
            RecipientRowState(
                id=str(recipient.pk),
                email=recipient.email,
                name=recipient.name,
                kind=recipient.kind,
                locale=recipient.locale,
                enabled=recipient.enabled,
                note=recipient.note,
                url=reverse("admin:messaging_systemrecipient_change", args=[recipient.pk]),
            )
            for recipient in qs[:200]
        ]
        return RecipientListState(
            create_url=reverse("admin:messaging_systemrecipient_add"),
            rows=rows,
            total_count=qs.count(),
        )

    def get_delivery_log_state(self, *, user: Any, filters: Mapping[str, Any] | None = None) -> DeliveryLogState:
        filters = filters or {}
        search_query = str(filters.get("q") or "").strip()
        qs = EmailLog.objects.order_by("-queued_at")
        if search_query:
            qs = qs.filter(
                Q(recipient__icontains=search_query)
                | Q(event_type__icontains=search_query)
                | Q(channel__icontains=search_query)
                | Q(status__icontains=search_query)
                | Q(subject__icontains=search_query)
                | Q(error_message__icontains=search_query)
                | Q(provider_message_id__icontains=search_query)
            )
        return DeliveryLogState(
            rows=[
                DeliveryLogRowState(
                    id=str(row.pk),
                    recipient=row.recipient,
                    event_type=row.event_type,
                    channel=row.channel,
                    status=row.status,
                    subject=row.subject,
                    queued_at=_display_datetime(row.queued_at),
                    sent_at=_display_datetime(row.sent_at),
                    error_message=row.error_message,
                    provider_message_id=row.provider_message_id,
                )
                for row in qs[:100]
            ]
        )

    def get_settings_state(self, *, user: Any) -> MessagingSettingsState:
        settings_obj = EmailSettings.load()
        fields = [
            "email_from",
            "email_sender_name",
            "email_reply_to",
            "site_base_url",
            "logo_url",
            "url_path_confirm",
            "url_path_cancel",
            "url_path_reschedule",
            "url_path_contact_form",
        ]
        return MessagingSettingsState(
            action_url=reverse("cabinet:messaging_settings"),
            sections=[
                MessagingSettingsSection(
                    key="identity",
                    title="Email identity",
                    fields=["email_from", "email_sender_name", "email_reply_to"],
                ),
                MessagingSettingsSection(
                    key="links",
                    title="Links",
                    fields=[
                        "site_base_url",
                        "logo_url",
                        "url_path_confirm",
                        "url_path_cancel",
                        "url_path_reschedule",
                        "url_path_contact_form",
                    ],
                ),
            ],
            values={field: getattr(settings_obj, field, "") for field in fields},
        )

    def reply_to_thread(self, *, user: Any, thread_id: str, body: str) -> MessagingActionResult:
        thread = get_thread_or_404(int(thread_id))
        create_reply(thread=thread, body=body, user=user)
        return self._ok("reply.sent", "Reply sent.", reverse("cabinet:messaging_detail", args=[thread.pk]))

    def mark_thread_read(self, *, user: Any, thread_id: str) -> MessagingActionResult:
        thread = get_thread_or_404(int(thread_id))
        mark_thread_read(thread=thread)
        return self._ok("thread.read", "Thread marked as read.", reverse("cabinet:messaging_detail", args=[thread.pk]))

    def mark_thread_processed(self, *, user: Any, thread_id: str) -> MessagingActionResult:
        thread = get_thread_or_404(int(thread_id))
        mark_thread_processed(thread=thread)
        return self._ok(
            "thread.processed",
            "Thread marked as processed.",
            reverse("cabinet:messaging_detail", args=[thread.pk]),
        )

    def mark_thread_spam(self, *, user: Any, thread_id: str) -> MessagingActionResult:
        thread = get_thread_or_404(int(thread_id))
        mark_thread_spam(thread=thread)
        return self._ok("thread.spam", "Thread marked as spam.", reverse("cabinet:messaging_inbox"))

    def archive_thread(self, *, user: Any, thread_id: str) -> MessagingActionResult:
        thread = get_thread_or_404(int(thread_id))
        archive_thread(thread=thread)
        return self._ok("thread.archived", "Thread archived.", reverse("cabinet:messaging_inbox"))

    def create_campaign(self, *, user: Any, payload: Mapping[str, Any]) -> MessagingActionResult:
        return MessagingActionResult(
            ok=False,
            code="campaign.admin_only",
            message="Campaigns are edited in Django admin.",
        )

    def update_campaign(self, *, user: Any, campaign_id: str, payload: Mapping[str, Any]) -> MessagingActionResult:
        return MessagingActionResult(
            ok=False,
            code="campaign.admin_only",
            message="Campaigns are edited in Django admin.",
        )

    def send_campaign(self, *, user: Any, campaign_id: str) -> MessagingActionResult:
        return MessagingActionResult(ok=False, code="campaign.admin_only", message="Campaign sending is not wired yet.")

    def send_test_campaign(self, *, user: Any, campaign_id: str, email: str) -> MessagingActionResult:
        return MessagingActionResult(
            ok=False,
            code="campaign.admin_only",
            message="Campaign test sending is not wired yet.",
        )

    def update_recipient(
        self, *, user: Any, recipient_id: str, payload: Mapping[str, Any]
    ) -> MessagingActionResult:
        return MessagingActionResult(
            ok=False,
            code="recipient.admin_only",
            message="Recipients are edited in Django admin.",
        )

    def update_settings(self, *, user: Any, payload: Mapping[str, Any]) -> MessagingActionResult:
        settings_obj = EmailSettings.load()
        for field_name in self.get_settings_state(user=user).values:
            setattr(settings_obj, field_name, str(payload.get(field_name, "")).strip())
        settings_obj.save()
        return self._ok("settings.saved", "Messaging settings saved.", reverse("cabinet:messaging_settings"))

    def _thread_state(self, thread: Thread) -> MailboxThreadState:
        prefetched_messages = getattr(thread, "_prefetched_objects_cache", {}).get("messages")
        first_message = (
            prefetched_messages[0]
            if prefetched_messages
            else thread.messages.order_by("created_at").first()
        )
        preview = first_message.body[:140] if first_message else ""
        return MailboxThreadState(
            id=str(thread.pk),
            url=reverse("cabinet:messaging_detail", args=[thread.pk]),
            subject=thread.subject or "(No subject)",
            preview=preview,
            sender_name=thread.sender_name,
            sender_email=thread.sender_email,
            sender_label=thread.sender_name or thread.sender_email,
            received_at=_display_datetime(thread.last_activity_at),
            status=thread.status,
            status_label=thread.get_status_display() if hasattr(thread, "get_status_display") else thread.status,
            unread=not thread.is_read,
            channel=thread.channel,
            topic=thread.topic,
            source=thread.source,
        )

    def _detail_state(self, thread: Thread) -> MailboxDetailState:
        thread_state = self._thread_state(thread)
        messages = [
            MessageState(
                id=str(message.pk),
                direction=message.direction,
                sender_label=message.sender_name or message.sender_email,
                recipient_label=message.recipient_email,
                subject=message.subject,
                body=message.body,
                created_at=_display_datetime(message.created_at),
                channel=message.channel,
            )
            for message in thread.messages.all()
        ]
        return MailboxDetailState(
            thread=thread_state,
            messages=messages,
            composer=ReplyComposerState(
                action_url=reverse("cabinet:messaging_thread_action", args=[thread.pk, "reply"]),
                placeholder="Write a reply...",
            ),
            actions=[
                MailboxActionState(
                    key="mark_processed",
                    label="Processed",
                    url=reverse("cabinet:messaging_thread_action", args=[thread.pk, "mark_processed"]),
                    icon="bi-check2-circle",
                    variant="success",
                ),
                MailboxActionState(
                    key="mark_spam",
                    label="Spam",
                    url=reverse("cabinet:messaging_thread_action", args=[thread.pk, "mark_spam"]),
                    icon="bi-exclamation-octagon",
                    variant="warning",
                ),
                MailboxActionState(
                    key="archive",
                    label="Archive",
                    url=reverse("cabinet:messaging_thread_action", args=[thread.pk, "archive"]),
                    icon="bi-archive",
                ),
            ],
        )

    def _campaign_status_filters(self, *, active: str) -> list[CampaignStatusSummaryState]:
        counts = Campaign.objects.aggregate(
            draft=Count("id", filter=Q(status="draft")),
            scheduled=Count("id", filter=Q(status="scheduled")),
            sent=Count("id", filter=Q(status="sent")),
            failed=Count("id", filter=Q(status="failed")),
        )
        definitions = [
            ("all", "All"),
            ("draft", "Draft"),
            ("scheduled", "Scheduled"),
            ("sent", "Sent"),
            ("failed", "Failed"),
        ]
        return [
            CampaignStatusSummaryState(
                key=key,
                label=label,
                count=Campaign.objects.count() if key == "all" else counts.get(key, 0) or 0,
                active=key == active,
                url=f"{reverse('cabinet:messaging_campaigns')}?status={key}",
            )
            for key, label in definitions
        ]

    @staticmethod
    def _ok(code: str, message: str, target_url: str) -> MessagingActionResult:
        return MessagingActionResult(ok=True, code=code, message=message, target_url=target_url)
