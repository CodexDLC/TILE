from codex_platform.workers.arq import CORE_FUNCTIONS

from workers.notification_worker.tasks.notification_tasks import (
    send_rendered_notification_task,
    send_universal_notification_task,
)

FUNCTIONS = [
    send_universal_notification_task,
    send_rendered_notification_task,
    *CORE_FUNCTIONS,
]
