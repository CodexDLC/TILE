from django.http import HttpRequest, HttpResponse
from django.utils import translation


class TechnicalRouteLocaleMiddleware:
    """Use browser locale preferences on non-prefixed cabinet and account routes."""

    route_prefixes = ("/cabinet/", "/accounts/")

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.path_info.startswith(self.route_prefixes):
            language = translation.get_language_from_request(request, check_path=False)
            translation.activate(language)
            request.LANGUAGE_CODE = translation.get_language()
        return self.get_response(request)
