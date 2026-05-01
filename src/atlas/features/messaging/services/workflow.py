from collections.abc import Iterable
from typing import Any

from django.db import transaction

from ..models import Message, MessageReply, Thread
from .alerts import notify_thread_reply


def create_manual_thread(*, to_email: str, subject: str, body: str, user: Any) -> Thread:
    display_name = user.get_full_name() if hasattr(user, "get_full_name") else ""
    sender_name = display_name or to_email

    with transaction.atomic():
        thread = Thread.objects.create(
            sender_name=sender_name,
            sender_email=to_email,
            subject=subject,
            topic="general",
            source="manual",
            channel="email",
            status=Thread.Status.PROCESSED,
            is_read=True,
        )
        message = Message.objects.create(
            thread=thread,
            direction=Message.Direction.OUTBOUND,
            sender_name=sender_name,
            sender_email=to_email,
            recipient_email=to_email,
            subject=subject,
            body=body,
            source=thread.source,
            channel=thread.channel,
        )
        MessageReply.objects.create(
            message=message,
            body=body,
            sent_by=user if getattr(user, "is_authenticated", False) else None,
            is_inbound=False,
        )
    return thread


def create_reply(*, thread: Thread, body: str, user: Any) -> MessageReply:
    with transaction.atomic():
        message = Message.objects.create(
            thread=thread,
            direction=Message.Direction.OUTBOUND,
            sender_name=getattr(user, "get_full_name", lambda: "")() or thread.sender_name,
            sender_email=thread.sender_email,
            recipient_email=thread.sender_email,
            subject=thread.subject,
            body=body,
            source=thread.source,
            channel=thread.channel,
        )
        reply = MessageReply.objects.create(
            message=message,
            body=body,
            sent_by=user if getattr(user, "is_authenticated", False) else None,
            is_inbound=False,
        )
        thread.status = Thread.Status.PROCESSED
        thread.is_read = True
        thread.save(update_fields=["status", "is_read", "last_activity_at"])
    notify_thread_reply(thread, reply)
    return reply


def mark_thread_read(*, thread: Thread) -> Thread:
    return _update_thread_state(thread=thread, is_read=True)


def mark_thread_unread(*, thread: Thread) -> Thread:
    return _update_thread_state(thread=thread, is_read=False)


def mark_thread_processed(*, thread: Thread) -> Thread:
    return _update_thread_state(thread=thread, status=Thread.Status.PROCESSED, is_read=True)


def mark_thread_open(*, thread: Thread) -> Thread:
    return _update_thread_state(thread=thread, status=Thread.Status.OPEN)


def mark_thread_spam(*, thread: Thread) -> Thread:
    return _update_thread_state(thread=thread, status=Thread.Status.SPAM, is_read=True)


def archive_thread(*, thread: Thread) -> Thread:
    return _update_thread_state(thread=thread, is_archived=True, is_read=True)


def apply_bulk_action(*, threads: Iterable[Thread], action: str) -> int:
    handlers = {
        "mark_read": mark_thread_read,
        "mark_unread": mark_thread_unread,
        "mark_processed": mark_thread_processed,
        "mark_open": mark_thread_open,
        "mark_spam": mark_thread_spam,
        "archive": archive_thread,
    }
    handler = handlers.get(action)
    if handler is None:
        raise ValueError(f"Unsupported bulk action: {action}")

    count = 0
    for thread in threads:
        handler(thread=thread)
        count += 1
    return count


def _update_thread_state(
    *,
    thread: Thread,
    status: str | None = None,
    is_read: bool | None = None,
    is_archived: bool | None = None,
) -> Thread:
    update_fields = ["last_activity_at"]
    if status is not None:
        thread.status = status
        update_fields.append("status")
    if is_read is not None:
        thread.is_read = is_read
        update_fields.append("is_read")
    if is_archived is not None:
        thread.is_archived = is_archived
        update_fields.append("is_archived")
    thread.save(update_fields=update_fields)
    return thread
