from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from system.models import EmailSettings

from ..models import EmailLog
from ..selectors import get_paginated_threads, get_status_counts, get_thread_or_404


@login_required
def inbox_view(request: HttpRequest) -> HttpResponse:
    status = request.GET.get("status", "all")
    page_obj = get_paginated_threads(status=status, page=request.GET.get("page"))
    context = {
        "page_obj": page_obj,
        "active_status": status,
        "status_counts": get_status_counts(),
    }
    return render(request, "cabinet/messaging/inbox.html", context)


@login_required
def detail_view(request: HttpRequest, pk: int) -> HttpResponse:
    thread = get_thread_or_404(pk)
    thread.is_read = True
    thread.save(update_fields=["is_read", "last_activity_at"])
    return render(request, "cabinet/messaging/detail.html", {"thread": thread})


@login_required
def templates_view(request: HttpRequest) -> HttpResponse:
    return render(request, "cabinet/messaging/templates.html")


@login_required
def log_view(request: HttpRequest) -> HttpResponse:
    logs = EmailLog.objects.order_by("-queued_at")[:50]
    return render(request, "cabinet/messaging/log.html", {"logs": logs})


@login_required
def settings_view(request: HttpRequest) -> HttpResponse:
    settings_obj = EmailSettings.load()
    field_names = [
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
    if request.method == "POST":
        for field_name in field_names:
            setattr(settings_obj, field_name, request.POST.get(field_name, "").strip())
        settings_obj.save()
        messages.success(request, "Messaging settings saved.")
        return redirect("cabinet:messaging_settings")

    return render(request, "cabinet/messaging/settings.html", {"email_settings": settings_obj})
