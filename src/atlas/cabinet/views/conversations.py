
from typing import Any

from django.http import HttpResponseNotFound, JsonResponse
from django.views import View


class _ConversationsDisabledView(View):
    def dispatch(self, request: Any, *args: Any, **kwargs: Any) -> HttpResponseNotFound:
        return HttpResponseNotFound("Conversations module is disabled in this scaffold.")


class InboxView(_ConversationsDisabledView):
    pass


class ProcessedView(_ConversationsDisabledView):
    pass


class AllMessagesView(_ConversationsDisabledView):
    pass


class ThreadView(_ConversationsDisabledView):
    pass


class ComposeView(_ConversationsDisabledView):
    pass


class ThreadReplyActionView(_ConversationsDisabledView):
    pass


class ThreadActionView(_ConversationsDisabledView):
    pass


class InboxBulkActionView(_ConversationsDisabledView):
    pass


def manual_check_view(request: Any) -> JsonResponse:
    return JsonResponse({"error": "Conversations module is disabled."}, status=404)
