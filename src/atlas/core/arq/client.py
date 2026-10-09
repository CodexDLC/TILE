from __future__ import annotations

from typing import Any

from arq.connections import create_pool
from asgiref.sync import async_to_sync
from codex_django.messaging import DjangoArqClient
from codex_platform.notifications.delivery import ArqNotificationAdapter


class AtlasArqClient:
    def enqueue(self, task_name: str, payload: dict[str, Any], *, queue_name: str | None = None) -> str | None:
        return async_to_sync(self.aenqueue)(task_name, payload, queue_name=queue_name)

    async def aenqueue(self, task_name: str, payload: dict[str, Any], *, queue_name: str | None = None) -> str | None:
        redis_settings = DjangoArqClient.build_redis_settings_from_django()
        pool = await create_pool(redis_settings)
        try:
            adapter = ArqNotificationAdapter(pool)
            if queue_name:
                job = await pool.enqueue_job(task_name, payload_dict=payload, _queue_name=queue_name)
                return getattr(job, "job_id", None)
            return await adapter.enqueue_async(task_name, payload)
        finally:
            await pool.aclose()


arq_client = AtlasArqClient()

__all__ = ["arq_client"]
