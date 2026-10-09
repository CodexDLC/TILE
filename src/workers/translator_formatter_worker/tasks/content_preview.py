from __future__ import annotations

import asyncio
import json
import re
from typing import Any

from loguru import logger as log
from redis.asyncio import Redis


async def smart_content_preview_task(ctx: dict[str, Any], payload_dict: dict[str, Any]) -> None:
    settings = ctx["settings"]
    redis = Redis.from_url(settings.redis_url, decode_responses=True)
    status_key = str(payload_dict["status_key"])
    result_key = str(payload_dict["result_key"])
    ttl = int(payload_dict.get("ttl_seconds") or 21600)
    languages = list(payload_dict.get("target_languages") or [])
    fields = list(payload_dict.get("fields") or [])

    try:
        await _write_json(
            redis,
            status_key,
            {
                "draft_id": payload_dict.get("draft_id"),
                "status": "running",
                "languages": [
                    {"language": language, "status": "pending", "fields": {}, "progress": 0} for language in languages
                ],
            },
            ttl,
        )

        language_results = []
        for index, language in enumerate(languages, start=1):
            await _write_json(
                redis,
                status_key,
                {
                    "draft_id": payload_dict.get("draft_id"),
                    "status": "running",
                    "languages": [
                        {
                            "language": item.get("language"),
                            "status": item.get("status"),
                            "fields": item.get("fields", {}),
                            "progress": item.get("progress", 0),
                        }
                        for item in language_results
                    ]
                    + [
                        {"language": language, "status": "running", "fields": {}, "progress": 40},
                        *[
                            {"language": pending_language, "status": "pending", "fields": {}, "progress": 0}
                            for pending_language in languages[index:]
                        ],
                    ],
                },
                ttl,
            )
            result_fields = await _process_language(
                settings=settings,
                fields=fields,
                base_language=str(payload_dict.get("base_language") or ""),
                target_language=str(language),
            )
            language_results.append(
                {
                    "language": language,
                    "status": "done",
                    "fields": result_fields,
                    "progress": 100,
                    "user_editable": True,
                }
            )

        result = {
            "draft_id": payload_dict.get("draft_id"),
            "status": "ready",
            "languages": language_results,
            "error": "",
        }
        await _write_json(redis, result_key, result, ttl)
        await _write_json(redis, status_key, result, ttl)
        log.info("SmartContentPreview | ready | draft_id={}", payload_dict.get("draft_id"))
    except Exception as exc:
        error_payload = {
            "draft_id": payload_dict.get("draft_id"),
            "status": "failed",
            "languages": [],
            "error": str(exc),
        }
        await _write_json(redis, result_key, error_payload, ttl)
        await _write_json(redis, status_key, error_payload, ttl)
        log.exception("SmartContentPreview | failed | draft_id={}", payload_dict.get("draft_id"))
    finally:
        await redis.aclose()


async def _process_language(
    *,
    settings: Any,
    fields: list[dict[str, Any]],
    base_language: str,
    target_language: str,
) -> dict[str, str]:
    ai_result = await _try_process_language_with_codex_ai(
        settings=settings,
        fields=fields,
        base_language=base_language,
        target_language=target_language,
    )
    if ai_result:
        return ai_result
    if not settings.ai_stub_when_unconfigured:
        return {}
    return _fallback_process_language(fields=fields, base_language=base_language, target_language=target_language)


async def _try_process_language_with_codex_ai(
    *,
    settings: Any,
    fields: list[dict[str, Any]],
    base_language: str,
    target_language: str,
) -> dict[str, str]:
    try:
        from codex_ai.core import LLMDispatcher, LLMRouter, PromptResult
        from codex_ai.core.protocol import LLMMessage
    except Exception:
        return {}

    provider = _build_ai_provider(settings)
    if provider is None:
        return {}

    router = LLMRouter()

    @router.prompt("content_language_preview")
    async def build_prompt(**_: Any) -> PromptResult:
        return PromptResult(
            system=(
                "You format and translate CMS content. Return only strict JSON object where keys are field names "
                "and values are strings. Preserve meaning. Fix spelling and punctuation. Do not add SEO fields."
            ),
            messages=[
                LLMMessage(
                    role="user",
                    content=json.dumps(
                        {
                            "base_language": base_language,
                            "target_language": target_language,
                            "fields": fields,
                        },
                        ensure_ascii=False,
                    ),
                )
            ],
            temperature=0.2,
        )

    dispatcher = LLMDispatcher(provider=provider)
    dispatcher.include_router(router)
    raw = await _process_ai_with_retries(
        dispatcher,
        settings=settings,
        target_language=target_language,
    )
    if raw is None:
        return {}
    field_names = {str(field.get("name") or "") for field in fields if field.get("name")}
    parsed = _parse_ai_json_result(str(raw), field_names=field_names)
    if not parsed:
        log.warning(
            "SmartContentPreview | ai parse failed | target_language={} | raw={}",
            target_language,
            str(raw).replace("\n", " ")[:500],
        )
    return parsed


async def _process_ai_with_retries(
    dispatcher: Any,
    *,
    settings: Any,
    target_language: str,
) -> str | None:
    max_retries = max(int(settings.ai_max_retries or 0), 0)
    attempts = max_retries + 1
    delay = max(float(settings.ai_retry_delay_seconds or 0), 0)

    for attempt in range(1, attempts + 1):
        try:
            return str(await dispatcher.process("content_language_preview"))
        except Exception as exc:
            can_retry = attempt < attempts and _is_retryable_ai_error(exc)
            log.warning(
                "SmartContentPreview | ai request failed | target_language={} | attempt={}/{} | retry={} | error={}",
                target_language,
                attempt,
                attempts,
                can_retry,
                exc,
            )
            if not can_retry:
                return None
            await asyncio.sleep(delay * attempt)
    return None


def _is_retryable_ai_error(exc: Exception) -> bool:
    message = str(exc).lower()
    return any(marker in message for marker in ("503", "unavailable", "429", "rate limit", "temporarily"))


def _parse_ai_json_result(raw: str, *, field_names: set[str]) -> dict[str, str]:
    for candidate in _json_candidates(raw):
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if not isinstance(parsed, dict):
            continue
        if isinstance(parsed.get("fields"), dict):
            parsed = parsed["fields"]
        result = {str(key): str(value) for key, value in parsed.items() if str(key) in field_names}
        if result:
            return result
    return {}


def _json_candidates(raw: str) -> list[str]:
    value = raw.strip()
    candidates = [value]

    fenced = re.search(r"```(?:json)?\s*(.*?)```", value, flags=re.IGNORECASE | re.DOTALL)
    if fenced:
        candidates.append(fenced.group(1).strip())

    first_brace = value.find("{")
    last_brace = value.rfind("}")
    if first_brace >= 0 and last_brace > first_brace:
        candidates.append(value[first_brace : last_brace + 1])

    return candidates


def _build_ai_provider(settings: Any) -> Any | None:
    provider_name = str(settings.ai_provider or "gemini").strip().lower()
    if provider_name in {"gemini", "google"}:
        api_key = str(settings.gemini_api_key or settings.google_api_key or "").strip()
        if not api_key:
            return None
        try:
            from codex_ai.providers import GeminiProvider
        except Exception as exc:
            log.warning("SmartContentPreview | gemini unavailable | error={}", exc)
            return None
        return GeminiProvider(api_key=api_key, model=str(settings.ai_model or "gemini-2.5-flash"))

    if provider_name == "openai":
        api_key = str(settings.openai_api_key or "").strip()
        if not api_key:
            return None
        try:
            from codex_ai.providers import OpenAIProvider
        except Exception as exc:
            log.warning("SmartContentPreview | openai unavailable | error={}", exc)
            return None
        return OpenAIProvider(api_key=api_key, model=str(settings.openai_model or settings.ai_model or "gpt-4o-mini"))

    log.warning("SmartContentPreview | unknown ai provider | provider={}", provider_name)
    return None


def _fallback_process_language(
    *,
    fields: list[dict[str, Any]],
    base_language: str,
    target_language: str,
) -> dict[str, str]:
    result = {}
    for field in fields:
        name = str(field.get("name") or "")
        value = str(field.get("value") or "").strip()
        if not name:
            continue
        if target_language == base_language:
            result[name] = _format_text(value)
        else:
            result[name] = f"[{target_language}] {_format_text(value)}"
    return result


def _format_text(value: str) -> str:
    if not value:
        return ""
    return " ".join(value.split())


async def _write_json(redis: Redis, key: str, payload: dict[str, Any], ttl: int) -> None:
    await redis.set(key, json.dumps(payload, ensure_ascii=False), ex=ttl)
