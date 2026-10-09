from loguru import logger as log


async def ensure_tasks_scheduled(ctx: dict) -> None:
    """Seed long-running periodic jobs when this worker starts.

    Atlas does not schedule domain-specific jobs here yet. Keep this hook as
    the common place for future worker-owned periodic tasks.
    """
    arq_service = ctx.get("arq_service")
    if not arq_service:
        log.warning("SystemWorker | seeding skipped: arq_service is missing")
        return
    log.debug("SystemWorker | no periodic system tasks registered")


async def system_watchdog_task(ctx: dict) -> None:
    log.info("SystemWorker | watchdog")
    await ensure_tasks_scheduled(ctx)
