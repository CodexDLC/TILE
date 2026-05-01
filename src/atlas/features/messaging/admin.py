from typing import ClassVar

from django.contrib import admin

from .models import Campaign, CampaignRecipient, EmailLog, Message, MessageReply, SystemRecipient, Thread


def _(message: str) -> str:
    return message


class MessageReplyInline(admin.TabularInline):
    model = MessageReply
    extra = 0
    fields = ("sent_by", "body", "is_inbound", "sent_at")
    readonly_fields = ("sent_at",)


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    fields = ("direction", "sender_name", "sender_email", "recipient_email", "subject", "body", "created_at")
    readonly_fields = ("created_at",)


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ("sender_name", "sender_email", "topic", "status", "source", "channel", "last_activity_at")
    list_filter = ("status", "topic", "source", "channel")
    search_fields = ("sender_name", "sender_email", "sender_phone", "subject")
    readonly_fields = ("thread_key", "created_at", "last_activity_at")
    inlines: ClassVar[list] = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("thread", "direction", "sender_email", "subject", "created_at")
    search_fields = ("sender_name", "sender_email", "subject", "body")
    readonly_fields = ("created_at", "updated_at")
    inlines: ClassVar[list] = [MessageReplyInline]


admin.site.register(MessageReply)
admin.site.register(SystemRecipient)
admin.site.register(EmailLog)
admin.site.register(Campaign)
admin.site.register(CampaignRecipient)
