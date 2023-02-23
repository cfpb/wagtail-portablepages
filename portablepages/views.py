from __future__ import annotations

from io import BytesIO

from django.http import FileResponse, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from wagtail.models import Page

from portablepages.forms import ImportForm
from portablepages.utils import export_page, import_page


def export_view(request: HttpRequest, page_id: int) -> FileResponse:
    page = get_object_or_404(Page, id=page_id).specific
    page_json = export_page(page)
    page_io = BytesIO(page_json.encode())
    response = FileResponse(
        page_io,
        as_attachment=True,
        filename=f"{page.slug}.json",
    )
    return response


def import_view(request: HttpRequest, page_id: int) -> HttpResponse:
    parent_page = get_object_or_404(Page, id=page_id).specific

    if request.method == "POST":
        input_form = ImportForm(request.POST, request.FILES)

        if input_form.is_valid():
            json_file = request.FILES["page_file"]
            new_page = import_page(
                parent_page, json_file.read().decode("utf8")
            )
            return redirect("wagtailadmin_pages:edit", new_page.id)
    else:
        input_form = ImportForm()

    return TemplateResponse(
        request,
        "portablepages/import_page.html",
        {
            "parent_page": parent_page,
            "form": input_form,
        },
    )
