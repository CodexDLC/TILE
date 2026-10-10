from __future__ import annotations

from typing import Any

from codex_django.cabinet import CabinetTemplateView, StaffRequiredMixin

from cabinet.services.users import UserService


class UserListView(StaffRequiredMixin, CabinetTemplateView):
    """
    Modular user list view for the cabinet dashboard.

    Supports 'segment' query parameter for smart filtering.
    Sets 'cabinet_module' on the request for topbar/sidebar active state.
    """

    template_name = "cabinet/users/list.html"
    cabinet_space = "staff"
    cabinet_module = "users"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(UserService.get_list_context(self.request))
        return context
