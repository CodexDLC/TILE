from codex_django.messaging.cabinet import MessagingCabinetPresenter, MessagingCabinetWorkflowService
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from ..bridge import AtlasMessagingBridge
from ..selectors import get_unread_count


def _bridge() -> AtlasMessagingBridge:
    return AtlasMessagingBridge()


def _presenter() -> MessagingCabinetPresenter:
    return MessagingCabinetPresenter()


def _with_table_search(
    request: HttpRequest,
    context: dict[str, object],
    table_key: str,
) -> dict[str, object]:
    table = context.get(table_key)
    if table is not None:
        table.search_query = request.GET.get("q", "").strip()
        table.search_action = request.path
    return context


def _render_messaging(
    request: HttpRequest,
    template_name: str,
    context: dict[str, object] | None = None,
) -> HttpResponse:
    request.cabinet_module = "messaging"  # type: ignore[attr-defined]
    data = {
        "unread_messages_count": get_unread_count(),
        **(context or {}),
    }
    return render(request, template_name, data)


@login_required
def inbox_view(request: HttpRequest) -> HttpResponse:
    bridge = _bridge()
    state = bridge.get_mailbox_state(
        user=request.user,
        folder=request.GET.get("folder", "inbox"),
        filters=request.GET,
    )
    return _render_messaging(request, "cabinet/messaging/pages/mailbox.html", _presenter().mailbox_context(state))


@login_required
def detail_view(request: HttpRequest, pk: int) -> HttpResponse:
    bridge = _bridge()
    MessagingCabinetWorkflowService(bridge).mark_read(user=request.user, thread_id=str(pk))
    state = bridge.get_mailbox_state(
        user=request.user,
        folder=request.GET.get("folder", "inbox"),
        thread_id=str(pk),
        filters=request.GET,
    )
    return _render_messaging(request, "cabinet/messaging/pages/mailbox.html", _presenter().mailbox_context(state))


@login_required
def thread_action_view(request: HttpRequest, pk: int, action: str) -> HttpResponse:
    if request.method != "POST":
        return redirect("cabinet:messaging_detail", pk=pk)
    result = MessagingCabinetWorkflowService(_bridge()).dispatch(
        action,
        user=request.user,
        thread_id=str(pk),
        payload=request.POST,
    )
    if result.ok:
        messages.success(request, result.message)
    else:
        messages.error(request, result.message)
    if result.target_url:
        return redirect(result.target_url)
    return redirect("cabinet:messaging_detail", pk=pk)


@login_required
def campaigns_view(request: HttpRequest) -> HttpResponse:
    state = _bridge().get_campaign_list_state(
        user=request.user,
        status=request.GET.get("status", "all"),
        filters=request.GET,
    )
    context = _with_table_search(request, _presenter().campaign_list_context(state), "campaigns_table")
    return _render_messaging(
        request,
        "cabinet/messaging/pages/campaigns.html",
        context,
    )


@login_required
def recipients_view(request: HttpRequest) -> HttpResponse:
    state = _bridge().get_recipient_list_state(user=request.user, filters=request.GET)
    context = _with_table_search(request, _presenter().recipient_list_context(state), "recipients_table")
    return _render_messaging(
        request,
        "cabinet/messaging/pages/recipients.html",
        context,
    )


@login_required
def delivery_log_view(request: HttpRequest) -> HttpResponse:
    state = _bridge().get_delivery_log_state(user=request.user, filters=request.GET)
    context = _with_table_search(request, _presenter().delivery_log_context(state), "delivery_log_table")
    return _render_messaging(
        request,
        "cabinet/messaging/pages/delivery_log.html",
        context,
    )


@login_required
def settings_view(request: HttpRequest) -> HttpResponse:
    bridge = _bridge()
    if request.method == "POST":
        result = MessagingCabinetWorkflowService(bridge).save_settings(user=request.user, payload=request.POST)
        if result.ok:
            messages.success(request, result.message)
            return redirect(result.target_url or "cabinet:messaging_settings")
        messages.error(request, result.message)

    state = bridge.get_settings_state(user=request.user)
    return _render_messaging(
        request,
        "cabinet/messaging/pages/settings.html",
        _presenter().settings_context(state),
    )
