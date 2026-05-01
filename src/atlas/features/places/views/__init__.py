from django.views.generic import TemplateView


class GridView(TemplateView):
    template_name = "places/grid_view.html"


class MapView(TemplateView):
    template_name = "places/map_view.html"


class SearchView(TemplateView):
    template_name = "places/search.html"
