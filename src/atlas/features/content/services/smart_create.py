from __future__ import annotations

from typing import Any

from codex_django.cabinet import (
    CabinetResource,
    SmartCreateJobRef,
    SmartCreateLanguageState,
    SmartCreateStatus,
)
from core.arq.client import arq_client
from core.redis import redis_manager
from django.conf import settings
from django.db import models

from features.content.models import ContentSmartDraft, ContentSmartDraftEvent

SMART_PREVIEW_TASK = "smart_content_preview_task"
SMART_PREVIEW_QUEUE = "translator_formatter"
SMART_PREVIEW_TTL_SECONDS = 60 * 60 * 6


class ContentSmartCreateHandler:
    def create_preview_job(
        self,
        *,
        resource: CabinetResource,
        user: Any,
        source_payload: dict[str, Any],
        base_language: str,
        target_languages: list[str] | tuple[str, ...],
    ) -> SmartCreateJobRef:
        languages = list(target_languages) or _default_target_languages(base_language)
        stored_source_payload = _json_safe_payload(source_payload)
        draft = ContentSmartDraft.objects.create(
            resource_key=resource.key,
            target_model=f"{resource.model._meta.app_label}.{resource.model._meta.model_name}",
            created_by=user if getattr(user, "is_authenticated", False) else None,
            base_language=base_language,
            target_languages=languages,
            source_payload=stored_source_payload,
            status=ContentSmartDraft.Status.PENDING,
        )
        ContentSmartDraftEvent.objects.create(draft=draft, status=draft.status, message="Preview job created")

        payload = {
            "draft_id": str(draft.pk),
            "resource_key": resource.key,
            "base_language": base_language,
            "target_languages": languages,
            "fields": _smart_fields(resource, stored_source_payload),
            "result_key": _draft_result_key(str(draft.pk)),
            "status_key": _draft_status_key(str(draft.pk)),
            "ttl_seconds": SMART_PREVIEW_TTL_SECONDS,
        }
        job_id = arq_client.enqueue(SMART_PREVIEW_TASK, payload=payload, queue_name=SMART_PREVIEW_QUEUE) or ""
        draft.arq_job_id = job_id
        draft.status = ContentSmartDraft.Status.RUNNING
        draft.save(update_fields=["arq_job_id", "status", "updated_at"])
        ContentSmartDraftEvent.objects.create(draft=draft, status=draft.status, message="Preview job enqueued")
        return SmartCreateJobRef(draft_id=str(draft.pk))

    def get_preview_status(
        self,
        *,
        resource: CabinetResource,
        draft_id: str,
        user: Any,
    ) -> SmartCreateStatus:
        draft = _get_user_draft(resource, draft_id, user)
        result_payload = _read_redis_json(_draft_result_key(draft_id))
        if result_payload:
            _sync_draft_result(draft, result_payload)
            return _status_from_payload(draft, result_payload)

        status_payload = _read_redis_json(_draft_status_key(draft_id))
        if status_payload:
            return _status_from_payload(draft, status_payload)

        return SmartCreateStatus(
            draft_id=str(draft.pk),
            status=draft.status,
            languages=[
                SmartCreateLanguageState(language=language, status="pending", progress=0)
                for language in draft.target_languages
            ],
            error=draft.error,
        )

    def publish(
        self,
        *,
        resource: CabinetResource,
        draft_id: str,
        user: Any,
        edited_payload: dict[str, Any],
    ) -> models.Model:
        draft = _get_user_draft(resource, draft_id, user)
        result_payload = _read_redis_json(_draft_result_key(draft_id)) or draft.result_payload
        language_fields = _merge_edited_payload(result_payload.get("languages", []), edited_payload)

        obj = resource.model()
        _apply_common_fields(obj, draft.source_payload)
        _apply_language_fields(obj, language_fields)
        obj.save()
        draft.mark_published(obj)
        ContentSmartDraftEvent.objects.create(draft=draft, status=draft.status, message="Draft published")
        return obj


def _default_target_languages(base_language: str) -> list[str]:
    languages = list(getattr(settings, "MODELTRANSLATION_LANGUAGES", ()))
    if base_language and base_language not in languages:
        languages.insert(0, base_language)
    return languages


def _smart_fields(resource: CabinetResource, source_payload: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "name": field.name,
            "label": field.label,
            "role": field.role,
            "format": field.format,
            "value": source_payload.get(field.name, ""),
        }
        for field in resource.form_fields
        if field.ai_enabled and field.name in source_payload
    ]


def _draft_result_key(draft_id: str) -> str:
    return f"atlas:smart-create:{draft_id}:result"


def _draft_status_key(draft_id: str) -> str:
    return f"atlas:smart-create:{draft_id}:status"


def _read_redis_json(key: str) -> dict[str, Any]:
    try:
        with redis_manager.sync_string() as string:
            raw = string.get(key)
    except Exception:
        return {}
    if not raw:
        return {}
    import json

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def _get_user_draft(resource: CabinetResource, draft_id: str, user: Any) -> ContentSmartDraft:
    queryset = ContentSmartDraft.objects.filter(pk=draft_id, resource_key=resource.key)
    if not getattr(user, "is_superuser", False):
        queryset = queryset.filter(created_by=user)
    return queryset.get()


def _sync_draft_result(draft: ContentSmartDraft, payload: dict[str, Any]) -> None:
    status = str(payload.get("status") or draft.status)
    error = str(payload.get("error") or "")
    update_fields: list[str] = []
    if draft.result_payload != payload:
        draft.result_payload = payload
        update_fields.append("result_payload")
    if status and draft.status != status:
        draft.status = status
        update_fields.append("status")
    if draft.error != error:
        draft.error = error
        update_fields.append("error")
    if update_fields:
        update_fields.append("updated_at")
        draft.save(update_fields=update_fields)


def _status_from_payload(draft: ContentSmartDraft, payload: dict[str, Any]) -> SmartCreateStatus:
    languages_payload = payload.get("languages") or []
    states = []
    if isinstance(languages_payload, list):
        for item in languages_payload:
            if not isinstance(item, dict):
                continue
            states.append(
                SmartCreateLanguageState(
                    language=str(item.get("language") or ""),
                    status=str(item.get("status") or "pending"),
                    fields=dict(item.get("fields") or {}),
                    error=str(item.get("error") or ""),
                    progress=int(item.get("progress") or 0),
                    user_editable=bool(item.get("user_editable", True)),
                )
            )
    return SmartCreateStatus(
        draft_id=str(draft.pk),
        status=str(payload.get("status") or draft.status),
        languages=states,
        error=str(payload.get("error") or draft.error),
    )


def _merge_edited_payload(languages: list[dict[str, Any]], edited_payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    merged = {
        str(language.get("language")): dict(language.get("fields") or {})
        for language in languages
        if isinstance(language, dict) and language.get("language")
    }
    for key, value in edited_payload.items():
        parts = key.split(".")
        if len(parts) != 3 or parts[0] != "languages":
            continue
        _, language, field_name = parts
        merged.setdefault(language, {})[field_name] = value
    return merged


def _apply_common_fields(obj: models.Model, source_payload: dict[str, Any]) -> None:
    translated_source_fields = {
        field.name.removesuffix(f"_{language}")
        for field in obj._meta.fields
        for language in getattr(settings, "MODELTRANSLATION_LANGUAGES", ())
        if field.name.endswith(f"_{language}")
    }
    for field_name, value in source_payload.items():
        if field_name in translated_source_fields:
            continue
        if not _has_model_field(obj, field_name):
            continue
        field = obj._meta.get_field(field_name)
        if getattr(field, "many_to_many", False):
            continue
        if isinstance(field, models.ForeignKey | models.OneToOneField):
            setattr(obj, f"{field_name}_id", value or None)
        else:
            setattr(obj, field_name, value)


def _apply_language_fields(obj: models.Model, language_fields: dict[str, dict[str, Any]]) -> None:
    for language, fields in language_fields.items():
        for field_name, value in fields.items():
            translated_name = f"{field_name}_{language}"
            if hasattr(obj, translated_name):
                setattr(obj, translated_name, value)
            elif language == getattr(settings, "MODELTRANSLATION_DEFAULT_LANGUAGE", "") and hasattr(obj, field_name):
                setattr(obj, field_name, value)


def _has_model_field(obj: models.Model, field_name: str) -> bool:
    try:
        obj._meta.get_field(field_name)
    except Exception:
        return False
    return True


def _json_safe_payload(payload: dict[str, Any]) -> dict[str, Any]:
    safe: dict[str, Any] = {}
    for key, value in payload.items():
        if isinstance(value, models.Model):
            safe[key] = value.pk
        else:
            safe[key] = value
    return safe
