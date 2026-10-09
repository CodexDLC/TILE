from codex_platform.workers.arq import CORE_FUNCTIONS

from workers.system_worker.tasks.maintenance import system_watchdog_task

FUNCTIONS = [
    system_watchdog_task,
    *CORE_FUNCTIONS,
]
