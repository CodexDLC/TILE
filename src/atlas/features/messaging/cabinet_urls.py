from django.urls import path

from .views import (
    campaigns_view,
    delivery_log_view,
    detail_view,
    inbox_view,
    recipients_view,
    settings_view,
    thread_action_view,
)

urlpatterns = [
    path("messaging/", inbox_view, name="messaging_inbox"),
    path("messaging/campaigns/", campaigns_view, name="messaging_campaigns"),
    path("messaging/recipients/", recipients_view, name="messaging_recipients"),
    path("messaging/delivery-log/", delivery_log_view, name="messaging_delivery_log"),
    path("messaging/settings/", settings_view, name="messaging_settings"),
    path("messaging/<int:pk>/<str:action>/", thread_action_view, name="messaging_thread_action"),
    path("messaging/<int:pk>/", detail_view, name="messaging_detail"),
]
