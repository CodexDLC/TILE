from django.utils.translation import get_language
from django.views.generic import TemplateView

from features.content.selectors.pages import get_homepage, get_page_context, get_page_template


class HomeView(TemplateView):
    def get_template_names(self) -> list[str]:
        page = self.get_page()
        return [get_page_template(page), "content/page_home.html"]

    def get_page(self):
        if not hasattr(self, "_page"):
            self._page = get_homepage(locale=get_language())
        return self._page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_page_context(self.get_page()))
        return context
