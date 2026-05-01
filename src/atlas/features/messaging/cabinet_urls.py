from django.urls import path

from .views import detail_view, inbox_view, log_view, settings_view, templates_view

urlpatterns = [
    path("messaging/", inbox_view, name="messaging_inbox"),
    path("messaging/<int:pk>/", detail_view, name="messaging_detail"),
    path("messaging/templates/", templates_view, name="messaging_templates"),
    path("messaging/log/", log_view, name="messaging_log"),
    path("messaging/settings/", settings_view, name="messaging_settings"),
]
