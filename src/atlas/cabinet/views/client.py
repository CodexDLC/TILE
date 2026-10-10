from typing import Any

from codex_django.cabinet import CabinetTemplateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from cabinet.services.client import ClientService


class ClientHomeView(LoginRequiredMixin, CabinetTemplateView):
    template_name = "cabinet/client/corner.html"
    cabinet_space = "client"
    cabinet_module = "client"

    def post(self, request: Any, *args: Any, **kwargs: Any) -> Any:
        success, message = ClientService.save_corner_profile(request)
        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(ClientService.get_corner_context(self.request))
        return context
