from django.urls import re_path

from .views import HomeView, PageDetailView

urlpatterns = [
    re_path(r"^$", HomeView.as_view(), name="home"),
    re_path(r"^(?P<path>.*)$", PageDetailView.as_view(), name="page-detail"),
]
