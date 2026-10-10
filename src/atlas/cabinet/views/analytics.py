from typing import Any

from codex_django.cabinet import CabinetTemplateView, StaffRequiredMixin
from codex_django.cabinet.views import dashboard_view
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from ..access import require_staff
from ..services.analytics import AnalyticsService


@login_required
def analytics_dashboard_view(request: Any) -> HttpResponse:
    """Wrapper for analytics dashboard to set active module."""
    require_staff(request.user)
    request.cabinet_space = "staff"
    request.cabinet_module = "analytics"
    return dashboard_view(request)


class AnalyticsReportsView(StaffRequiredMixin, CabinetTemplateView):
    """Страница детальных отчетов."""

    template_name = "cabinet/analytics/reports.html"

    cabinet_space = "staff"
    cabinet_module = "analytics"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # Получаем данные детальных отчетов
        context.update(AnalyticsService.get_reports_context(self.request))
        return context
