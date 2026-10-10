from django.conf import settings
from django.urls import include, path
from features.content.views.editor import article_edit, article_list, article_preview

from .views.analytics import AnalyticsReportsView, analytics_dashboard_view
from .views.client import ClientHomeView
from .views.resources import resource_edit_view
from .views.users import UserListView

app_name = "cabinet"

urlpatterns = [
    path("articles/", article_list, name="article_list"),
    path("articles/new/", article_edit, name="article_create"),
    path("articles/<int:pk>/edit/", article_edit, name="article_edit"),
    path("articles/<int:pk>/preview/", article_preview, name="article_preview"),
    path("resources/<str:resource_key>/<str:pk>/edit/", resource_edit_view, name="resource_edit"),
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
