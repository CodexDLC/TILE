from typing import Any

from django.core.paginator import Page, Paginator
from django.db.models import Count, Prefetch, Q, QuerySet
from django.shortcuts import get_object_or_404

from ..models import Message, MessageReply, Thread


def get_thread_queryset() -> QuerySet[Thread]:
    return Thread.objects.filter(is_archived=False).order_by("-last_activity_at")


def get_threads(*, status: str | None = None, topic: str | None = None) -> QuerySet[Thread]:
    qs = get_thread_queryset()
    if status and status != "all":
        qs = qs.filter(status=status)
    if topic:
        qs = qs.filter(topic=topic)
    return qs


def get_thread_or_404(pk: int) -> Thread:
    return get_object_or_404(
        get_thread_queryset().prefetch_related(
            Prefetch("messages", queryset=Message.objects.order_by("created_at").prefetch_related("replies"))
        ),
        pk=pk,
    )


def get_status_counts() -> dict[str, int]:
    return Thread.objects.filter(is_archived=False).aggregate(
        open=Count("id", filter=Q(status=Thread.Status.OPEN)),
        processed=Count("id", filter=Q(status=Thread.Status.PROCESSED)),
        spam=Count("id", filter=Q(status=Thread.Status.SPAM)),
    )


def get_topic_counts() -> list[dict[str, Any]]:
    return list(
        Thread.objects.filter(is_archived=False)
        .exclude(status=Thread.Status.SPAM)
        .values("topic")
        .annotate(count=Count("id"))
        .order_by("topic")
    )


def get_unread_count() -> int:
    return Thread.objects.filter(is_archived=False, is_read=False).count()


def get_paginated_threads(
    *,
    status: str | None = None,
    topic: str | None = None,
    page: str | int | None = None,
    per_page: int = 50,
) -> Page[Thread]:
    return Paginator(get_threads(status=status, topic=topic), per_page).get_page(page)


def get_replies(message_id: int) -> QuerySet[MessageReply]:
    return MessageReply.objects.filter(message_id=message_id).select_related("sent_by").order_by("sent_at")
