from django.urls import path

from .views import GridView, MapView, SearchView

urlpatterns = [
    path("grid/", GridView.as_view(), name="places-grid"),
    path("map/", MapView.as_view(), name="places-map"),
    path("search/", SearchView.as_view(), name="places-search"),
]
