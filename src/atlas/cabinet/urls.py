from django.conf import settings
from django.urls import include, path

from .views.analytics import AnalyticsReportsView, analytics_dashboard_view
from .views.client import ClientHomeView
from .views.site_settings import site_settings_tab_view, site_settings_view
from .views.users import UserListView

app_name = "cabinet"

urlpatterns = [
    path("site/settings/", site_settings_view, name="site_settings"),
    path("site/settings/<str:tab_slug>/", site_settings_tab_view, name="site_settings_tab"),
    # Codex cabinet library: dashboard + generic routes
    path("", include("codex_django.cabinet.urls")),
    path("", include("cabinet.auth_urls")),
    path("", include("features.messaging.cabinet_urls")),
    path("my/", ClientHomeView.as_view(), name="client_home"),
    path("analytics/", analytics_dashboard_view, name="analytics_dashboard"),
    path("analytics/reports/", AnalyticsReportsView.as_view(), name="analytics_reports"),
    # Users / Clients
    path("users/", UserListView.as_view(), name="users_list"),
]

if getattr(settings, "CODEX_ALLAUTH_ENABLED", False):
    urlpatterns.insert(2, path("", include("allauth.urls")))
