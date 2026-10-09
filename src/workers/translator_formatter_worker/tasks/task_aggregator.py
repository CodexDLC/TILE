from codex_platform.workers.arq import CORE_FUNCTIONS

from workers.translator_formatter_worker.tasks.content_preview import smart_content_preview_task

FUNCTIONS = [
    smart_content_preview_task,
    *CORE_FUNCTIONS,
]
