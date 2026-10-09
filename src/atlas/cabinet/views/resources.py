from __future__ import annotations

from dataclasses import replace
from typing import Any

from codex_django.cabinet.resources import CabinetResource, CabinetResourceField, cabinet_resource_registry
from codex_django.cabinet.resources.forms import build_resource_form_class
from codex_django.cabinet.resources.services import require_resource_permission
from codex_django.cabinet.resources.urls import resource_url
from django import forms
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render


@login_required
def resource_edit_view(request: HttpRequest, resource_key: str, pk: str) -> HttpResponse:
    """Edit resource instances with all modeltranslation fields visible."""
    resource = cabinet_resource_registry.get(resource_key)
    _attach_cabinet_metadata(request, resource.section)
    require_resource_permission(request.user, resource, "edit")

    obj = get_object_or_404(resource.model, pk=pk)
    edit_resource = _build_edit_resource(resource)
    form_class = build_resource_form_class(edit_resource)
    form = form_class(request.POST if request.method == "POST" else None, request.FILES or None, instance=obj)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(resource_url("resource_list", resource_key=resource.key))

    language_groups, plain_fields = _build_form_layout(form, resource, edit_resource)
    return render(
        request,
        "cabinet/resources/form.html",
        {
            "resource": resource,
            "title": f"Редактировать {resource.singular_title}",
            "form": form,
            "plain_fields": plain_fields,
            "translation_groups": language_groups,
            "object": obj,
            "list_url": resource_url("resource_list", resource_key=resource.key),
        },
    )


def _build_edit_resource(resource: CabinetResource) -> CabinetResource:
    fields: list[CabinetResourceField] = []
    for field in resource.form_fields:
        translated_fields = _translation_field_specs(resource.model, field)
        fields.extend(translated_fields or [field])
    return replace(resource, form_fields=tuple(fields))


def _translation_field_specs(model: type[models.Model], field: CabinetResourceField) -> list[CabinetResourceField]:
    if field.virtual:
        return []
    if not _is_translatable_model_field(model, field.name):
        return []

    specs = []
    for language_code, language_label in _translation_languages():
        translated_name = f"{field.name}_{language_code}"
        if _has_model_field(model, translated_name):
            specs.append(replace(field, name=translated_name, label=f"{field.label or field.name} ({language_label})"))
    return specs


def _is_translatable_model_field(model: type[models.Model], field_name: str) -> bool:
    languages = [language_code for language_code, _label in _translation_languages()]
    return bool(languages) and any(
        _has_model_field(model, f"{field_name}_{language_code}") for language_code in languages
    )


def _translation_languages() -> list[tuple[str, str]]:
    language_labels = dict(getattr(settings, "LANGUAGES", ()))
    language_codes = tuple(getattr(settings, "MODELTRANSLATION_LANGUAGES", ())) or tuple(language_labels)
    return [(code, str(language_labels.get(code, code.upper()))) for code in language_codes]


def _has_model_field(model: type[models.Model], field_name: str) -> bool:
    try:
        model._meta.get_field(field_name)
    except Exception:
        return False
    return True


def _build_form_layout(
    form: forms.BaseForm,
    source_resource: CabinetResource,
    edit_resource: CabinetResource,
) -> tuple[list[dict[str, Any]], list[forms.BoundField]]:
    translated_names = {
        f"{field.name}_{language_code}"
        for field in source_resource.form_fields
        for language_code, _label in _translation_languages()
        if _is_translatable_model_field(source_resource.model, field.name)
    }
    plain_fields = [form[field.name] for field in edit_resource.form_fields if field.name not in translated_names]
    language_groups = []

    for language_code, language_label in _translation_languages():
        fields = [
            form[f"{field.name}_{language_code}"]
            for field in source_resource.form_fields
            if f"{field.name}_{language_code}" in form.fields
        ]
        if fields:
            language_groups.append({"code": language_code, "label": language_label, "fields": fields})

    return language_groups, plain_fields


def _attach_cabinet_metadata(request: HttpRequest, section: str) -> None:
    request.cabinet_space = "staff"
    request.cabinet_module = section.lower().replace(" ", "_") or "resources"
