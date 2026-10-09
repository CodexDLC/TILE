from codex_core.common.loguru_setup import setup_logging
from codex_platform.workers.arq import BaseArqWorkerSettings, base_shutdown, base_startup
from loguru import logger as log

from workers.core.config import WorkerSettings as CoreWorkerSettings
from workers.translator_formatter_worker.tasks.task_aggregator import FUNCTIONS

settings = CoreWorkerSettings()


async def worker_startup(ctx: dict) -> None:
    setup_logging(settings, "translator_formatter_worker")
    ctx["settings"] = settings
    await base_startup(ctx)
    log.info("TranslatorFormatterWorker | startup complete")


async def worker_shutdown(ctx: dict) -> None:
    log.info("TranslatorFormatterWorker | shutdown")
    await base_shutdown(ctx)


class WorkerSettings(BaseArqWorkerSettings):
    redis_settings = settings.arq_redis_settings
    max_jobs = settings.arq_max_jobs
    job_timeout = settings.arq_job_timeout
    keep_result = settings.arq_keep_result
    queue_name = "translator_formatter"
    on_startup = worker_startup
    on_shutdown = worker_shutdown
    functions = FUNCTIONS
