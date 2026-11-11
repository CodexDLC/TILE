from django.urls import path, re_path
from django.views.generic import TemplateView

from .views import HomeView, PageDetailView

urlpatterns = [
    re_path(r"^$", HomeView.as_view(), name="home"),
    path("about/", TemplateView.as_view(template_name="content/project_concept.html"), name="project-concept"),
    re_path(r"^(?P<path>.*)$", PageDetailView.as_view(), name="page-detail"),
]
