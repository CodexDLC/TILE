from django.shortcuts import redirect
from django.views.generic import TemplateView


class GridView(TemplateView):
    def get(self, request, *args, **kwargs):
        return _redirect_to_search(request)


class MapView(TemplateView):
    def get(self, request, *args, **kwargs):
        return _redirect_to_search(request)


def _redirect_to_search(request):
    response = redirect("places-search")
    query = request.META.get("QUERY_STRING", "")
    return response if not query else redirect(f"{response.url}?{query}")


class SearchView(TemplateView):
    template_name = "places/search.html"

    def get_context_data(self, **kwargs):
        from django.core.paginator import Paginator

        from features.content.selectors.articles import search_pages

        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q", "").strip()[:200]
        context["query"] = query
        context["results"] = Paginator(search_pages(query), 18).get_page(self.request.GET.get("page"))
        return context

