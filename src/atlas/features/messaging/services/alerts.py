import logging
from functools import lru_cache

from codex_django.messaging import (
    BaseMessagingEngine,
    DjangoQueueAdapter,
    NotificationDispatchSpec,
    email_rendered,
    notification_handler,
)
from django.conf import settings

from .adapter import AtlasMessagingDirectAdapter


def _(message: str) -> str:
    return message


log = logging.getLogger(__name__)
_HAS_ARQ = bool(getattr(settings, "ARQ_REDIS_URL", None) or getattr(settings, "REDIS_URL", None))


def notify_new_message(thread) -> None:
    try:
        _get_messaging_engine().dispatch_event("messaging.new_message", thread)
    except Exception:
        log.exception("Failed to dispatch new message notification for thread_id=%s", thread.pk)


def notify_thread_reply(thread, reply) -> None:
    try:
        _get_messaging_engine().dispatch_event("messaging.thread_reply", thread, reply)
    except Exception:
        log.exception("Failed to dispatch thread reply notification for thread_id=%s", thread.pk)


class _StaticSubjectSelector:
    def get(self, key: str, language: str = "de") -> str | None:
        return None


@lru_cache(maxsize=1)
def _get_messaging_engine() -> BaseMessagingEngine:
    return BaseMessagingEngine(
        queue_adapter=_build_queue_adapter(),
        cache_adapter=None,
        i18n_adapter=None,
        selector=_StaticSubjectSelector(),
    )


def _build_queue_adapter():
    if _HAS_ARQ:
        try:
            from core.arq.client import arq_client

            return DjangoQueueAdapter(arq_client=arq_client)
        except Exception:
            log.warning("ARQ configured but project arq client is unavailable, using direct adapter", exc_info=True)
    return AtlasMessagingDirectAdapter()


@notification_handler("messaging.new_message")
def _build_new_message_specs(thread):
    return list(_iter_admin_specs(thread))


@email_rendered("messaging.thread_reply")
def _build_thread_reply_payload(thread=None, reply=None):
    if thread is None or reply is None:
        return {
            "recipient_email": "placeholder@example.com",
            "subject_key": "messaging.thread_reply.subject",
            "html_content": "<p></p>",
        }
    return {
        "recipient_email": thread.sender_email,
        "subject_key": "messaging.thread_reply.subject",
        "subject": _build_reply_subject(thread),
        "html_content": f"<p>{reply.body}</p>",
        "text_content": reply.body,
        "context": {"thread_id": thread.pk, "reply_id": reply.pk, "thread_key": thread.thread_key},
    }


def build_admin_specs(thread) -> list[NotificationDispatchSpec]:
    return list(_iter_admin_specs(thread))


def _iter_admin_specs(thread):
    for _, email in getattr(settings, "ADMINS", ()):
        if not email:
            continue
        yield NotificationDispatchSpec(
            recipient_email=email,
            subject_key="messaging.new_message.subject",
            event_type="messaging.new_message",
            channels=["email"],
            subject=_build_subject(thread),
            mode="rendered",
            html_content=f"<pre>{_build_text_content(thread)}</pre>",
            text_content=_build_text_content(thread),
            context={"thread_id": thread.pk, "thread_key": thread.thread_key},
        )


def _build_subject(thread) -> str:
    preview = thread.subject or _get_root_message_text(thread)[:60]
    return _("[New message] %(sender)s - %(preview)s") % {
        "sender": thread.sender_name,
        "preview": preview,
    }


def _build_text_content(thread) -> str:
    return _(
        "From: %(name)s <%(email)s>\n"
        "Topic: %(topic)s\n"
        "Source: %(source)s\n"
        "Channel: %(channel)s\n\n"
        "%(body)s"
    ) % {
        "name": thread.sender_name,
        "email": thread.sender_email,
        "topic": thread.topic,
        "source": thread.source,
        "channel": thread.channel,
        "body": _get_root_message_text(thread),
    }


def _get_root_message_text(thread) -> str:
    first_message = thread.messages.order_by("created_at").first()
    return first_message.body if first_message else ""


def _build_reply_subject(thread) -> str:
    subject = thread.subject.strip() if thread.subject else ""
    if not subject:
        return _("Re: Conversation %(thread)s") % {"thread": thread.thread_key[:8]}
    if subject.lower().startswith("re:"):
        return subject
    return _("Re: %(subject)s") % {"subject": subject}
