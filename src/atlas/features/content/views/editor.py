from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods

from features.content.forms.articles import LANGUAGES, ArticleForm
from features.content.selectors.articles import article_language, article_parts, articles, get_article, raw_translation
from features.content.selectors.pages import get_page_context, get_page_template
from features.content.services.articles import require_author, save_article, unpublish_article


def _metadata(request):
    request.cabinet_space = "staff"
    request.cabinet_module = "content"


@login_required
@require_http_methods(["GET"])
def article_list(request):
    require_author(request.user, "view")
    _metadata(request)
    queryset = articles().order_by("-updated_at", "-pk")
    status = request.GET.get("status", "")
    if status in {"draft", "published"}:
        queryset = queryset.filter(is_published=status == "published")
    return render(
        request,
        "cabinet/articles/list.html",
        {
            "articles": Paginator(queryset, 20).get_page(request.GET.get("page")),
            "status": status,
        },
    )


@login_required
@never_cache
@require_http_methods(["GET", "POST"])
def article_edit(request, pk=None):
    require_author(request.user, "change" if pk else "add")
    _metadata(request)
    page = get_article(pk) if pk else None
    language = (
        request.POST.get("language") or request.GET.get("language") or (article_language(page, "ru") if page else "ru")
    )
    if language not in dict(LANGUAGES):
        language = "ru"
    if request.method == "POST" and request.POST.get("action") == "unpublish" and page:
        unpublish_article(user=request.user, page=page)
        messages.success(request, _("The article was unpublished and saved as a draft."))
        return redirect("cabinet:article_list")
    form = ArticleForm(
        request.POST if request.method == "POST" else None, request.FILES or None, page=page, language=language
    )
    if request.method == "POST" and form.is_valid():
        page = save_article(
            user=request.user, data=form.cleaned_data, page=page, publish=request.POST.get("action") == "publish"
        )
        messages.success(request, _("Article published.") if page.is_published else _("Draft saved."))
        destination = "article_preview" if request.POST.get("action") == "preview" else "article_edit"
        return HttpResponseRedirect(reverse("cabinet:" + destination, args=[page.pk]) + "?language=" + language)
    return render(
        request,
        "cabinet/articles/form.html",
        {
            "form": form,
            "article": page,
            "language": language,
            "languages": LANGUAGES,
            "cover": article_parts(page)["cover"],
        },
    )


@login_required
@never_cache
@require_http_methods(["GET"])
def article_preview(request, pk):
    require_author(request.user, "view")
    page = get_article(pk)
    context = get_page_context(page)
    context["is_preview"] = True
    preferred = request.GET.get("language")
    if preferred in dict(LANGUAGES):
        context["article_language"] = article_language(page, preferred)
        language = context["article_language"]
        context["article_title"] = raw_translation(page, "title", language)
        context["article_intro"] = raw_translation(page, "intro", language)
        context["article_meta_title"] = raw_translation(page, "seo_title", language) or context["article_title"]
        context["article_meta_description"] = (
            raw_translation(page, "seo_description", language) or context["article_intro"]
        )
    response = render(request, get_page_template(page), context)
    response["X-Robots-Tag"] = "noindex, nofollow, noarchive"
    return response



