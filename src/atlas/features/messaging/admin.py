from typing import ClassVar

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin, TabularInline

from .models import Campaign, CampaignRecipient, EmailLog, Message, MessageReply, SystemRecipient, Thread


class MessageReplyInline(TabularInline):
    model = MessageReply
    extra = 0
    fields = ("sent_by", "is_inbound", "body", "sent_at")
    readonly_fields = ("sent_at",)
    ordering = ("sent_at",)


class MessageInline(TabularInline):
    model = Message
    extra = 0
    fields = ("direction", "sender_name", "sender_email", "recipient_email", "subject", "created_at")
    readonly_fields = ("created_at",)
    ordering = ("created_at",)


class CampaignRecipientInline(TabularInline):
    model = CampaignRecipient
    extra = 0
    fields = ("email", "locale", "status", "notification_id", "provider_message_id", "updated_at")
    readonly_fields = ("updated_at",)
    ordering = ("-updated_at",)


@admin.register(Thread)
class ThreadAdmin(ModelAdmin):
    list_display = (
        "sender_name",
        "sender_email",
        "subject",
        "topic",
        "status",
        "channel",
        "is_read",
        "is_archived",
        "last_activity_at",
    )
    list_filter = ("status", "topic", "source", "channel", "is_read", "is_archived")
    search_fields = ("sender_name", "sender_email", "sender_phone", "subject", "thread_key")
    readonly_fields = ("thread_key", "created_at", "last_activity_at")
    date_hierarchy = "last_activity_at"
    list_filter_submit = True
    inlines: ClassVar[list] = [MessageInline]
    fieldsets = (
        (
            _("Thread"),
            {
                "fields": (
                    "thread_key",
                    "subject",
                    "status",
                    "topic",
                    "source",
                    "channel",
                )
            },
        ),
        (
            _("Sender"),
            {
                "fields": (
                    "sender_name",
                    "sender_email",
                    "sender_phone",
                )
            },
        ),
        (
            _("State"),
            {
                "fields": (
                    "is_read",
                    "is_archived",
                    "created_at",
                    "last_activity_at",
                )
            },
        ),
    )


@admin.register(Message)
class MessageAdmin(ModelAdmin):
    list_display = ("thread", "direction", "sender_email", "recipient_email", "subject", "source", "channel", "created_at")
    list_filter = ("direction", "source", "channel", "created_at")
    search_fields = ("sender_name", "sender_email", "recipient_email", "subject", "body", "message_id_header")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"
    autocomplete_fields = ("thread",)
    list_filter_submit = True
    inlines: ClassVar[list] = [MessageReplyInline]
    fieldsets = (
        (
            _("Message"),
            {
                "fields": (
                    "thread",
                    "direction",
                    "subject",
                    "body",
                )
            },
        ),
        (
            _("Participants"),
            {
                "fields": (
                    "sender_name",
                    "sender_email",
                    "recipient_email",
                )
            },
        ),
        (
            _("Transport"),
            {
                "fields": (
                    "source",
                    "channel",
                    "message_id_header",
                    "in_reply_to_header",
                    "references_header",
                ),
                "classes": ("tab",),
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(MessageReply)
class MessageReplyAdmin(ModelAdmin):
    list_display = ("message", "sent_by", "is_inbound", "sent_at")
    list_filter = ("is_inbound", "sent_at")
    search_fields = ("body", "sent_by__username", "sent_by__email", "message__subject", "message__sender_email")
    readonly_fields = ("created_at", "sent_at")
    autocomplete_fields = ("message", "sent_by")
    date_hierarchy = "sent_at"
    fieldsets = (
        (
            _("Reply"),
            {
                "fields": (
                    "message",
                    "sent_by",
                    "is_inbound",
                    "body",
                )
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": ("created_at", "sent_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(SystemRecipient)
class SystemRecipientAdmin(ModelAdmin):
    list_display = ("email", "name", "kind", "locale", "enabled")
    list_filter = ("kind", "locale", "enabled")
    search_fields = ("email", "name", "note")
    fieldsets = (
        (
            _("Recipient"),
            {
                "fields": (
                    "email",
                    "name",
                    "kind",
                    "locale",
                    "enabled",
                    "note",
                )
            },
        ),
        (
            _("Delivery"),
            {
                "fields": ("unsubscribe_token",),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(EmailLog)
class EmailLogAdmin(ModelAdmin):
    list_display = ("notification_id", "event_type", "channel", "recipient", "status", "queued_at", "sent_at")
    list_filter = ("status", "channel", "event_type", "queued_at")
    search_fields = ("notification_id", "recipient", "subject", "provider_message_id", "message_id_header")
    readonly_fields = (
        "notification_id",
        "event_type",
        "channel",
        "recipient",
        "status",
        "subject",
        "error_message",
        "context_preview",
        "provider_message_id",
        "message_id_header",
        "queued_at",
        "sent_at",
    )
    date_hierarchy = "queued_at"
    list_filter_submit = True
    fieldsets = (
        (
            _("Delivery log"),
            {
                "fields": (
                    "notification_id",
                    "event_type",
                    "channel",
                    "recipient",
                    "status",
                    "subject",
                )
            },
        ),
        (
            _("Provider data"),
            {
                "fields": (
                    "provider_message_id",
                    "message_id_header",
                    "context_preview",
                    "error_message",
                ),
                "classes": ("tab",),
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": ("queued_at", "sent_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def has_add_permission(self, request):
        return False


@admin.register(Campaign)
class CampaignAdmin(ModelAdmin):
    list_display = ("subject", "status", "locale", "created_by", "send_at", "sent_at", "updated_at")
    list_filter = ("status", "locale", "created_at", "send_at", "sent_at")
    search_fields = ("subject", "template_key", "body_text", "arq_parent_job_id")
    readonly_fields = ("created_at", "updated_at", "sent_at")
    autocomplete_fields = ("created_by",)
    date_hierarchy = "created_at"
    list_filter_submit = True
    inlines: ClassVar[list] = [CampaignRecipientInline]
    fieldsets = (
        (
            _("Campaign"),
            {
                "fields": (
                    "subject",
                    "status",
                    "locale",
                    "template_key",
                    "body_text",
                    "body_translations",
                    "audience_filter",
                )
            },
        ),
        (
            _("Scheduling"),
            {
                "fields": (
                    "created_by",
                    "send_at",
                    "sent_at",
                    "arq_parent_job_id",
                )
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(CampaignRecipient)
class CampaignRecipientAdmin(ModelAdmin):
    list_display = ("campaign", "email", "locale", "status", "notification_id", "updated_at")
    list_filter = ("status", "locale", "created_at", "updated_at")
    search_fields = ("email", "first_name", "last_name", "recipient_id", "notification_id", "provider_message_id")
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("campaign",)
    date_hierarchy = "created_at"
    list_filter_submit = True
    fieldsets = (
        (
            _("Recipient"),
            {
                "fields": (
                    "campaign",
                    "recipient_id",
                    "email",
                    "first_name",
                    "last_name",
                    "locale",
                )
            },
        ),
        (
            _("Delivery state"),
            {
                "fields": (
                    "status",
                    "notification_id",
                    "provider_message_id",
                    "unsubscribe_token",
                    "arq_job_id",
                    "error_message",
                )
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
