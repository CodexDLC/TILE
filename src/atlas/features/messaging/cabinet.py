from codex_django.cabinet import DashboardWidget, MetricWidgetData, declare
from codex_django.cabinet.notifications import notification_registry
from codex_django.cabinet.selector.dashboard import DashboardSelector
from codex_django.messaging.cabinet import build_messaging_sidebar, build_messaging_topbar
from django.http import HttpRequest
from django.urls import reverse, reverse_lazy

from .selectors import get_status_counts, get_unread_count


def _(message: str) -> str:
    return message


@notification_registry.register("messaging")  # type: ignore[untyped-decorator]
def _messaging_bell(request: HttpRequest) -> object:
    return {
        "count": get_unread_count(),
        "url": reverse("cabinet:messaging_inbox"),
        "label": str(_("New messages")),
        "icon": "bi-envelope",
    }


@DashboardSelector.extend(cache_key="messaging_stats", cache_ttl=0)  # type: ignore[untyped-decorator]
def provide_messaging_stats(request: HttpRequest) -> dict[str, MetricWidgetData]:
    counts = get_status_counts()
    return {
        "messaging_stats": MetricWidgetData(
            label=str(_("Messages")),
            value=str(counts["open"] + counts["processed"]),
            trend_value=f"{_('waiting')}: {counts['open']}",
            trend_label=str(_("no response yet")),
            icon="bi-chat-dots",
            url=reverse("cabinet:messaging_inbox"),
        )
    }


declare(
    module="messaging",
    space="staff",
    topbar=build_messaging_topbar(reverse_lazy("cabinet:messaging_inbox"), label=str(_("Messaging"))),
    sidebar=build_messaging_sidebar(
        mailbox_url=reverse_lazy("cabinet:messaging_inbox"),
        campaigns_url=reverse_lazy("cabinet:messaging_campaigns"),
        recipients_url=reverse_lazy("cabinet:messaging_recipients"),
        delivery_log_url=reverse_lazy("cabinet:messaging_delivery_log"),
    ),
    settings_url="cabinet:messaging_settings",
    dashboard_widgets=[
        DashboardWidget(
            template="cabinet/widgets/kpi.html",
            context_key="messaging_stats",
            order=1,
            col="col-lg-3",
            nav_group="services",
        )
    ],
)
