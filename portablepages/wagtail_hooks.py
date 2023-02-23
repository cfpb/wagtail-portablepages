from typing import List, Optional

from django.urls import path, reverse
from django.urls.resolvers import URLPattern

from wagtail import hooks
from wagtail.admin.widgets import Button
from wagtail.models import Page, PagePermissionTester

from portablepages.views import export_view, import_view


def page_listing_import_button(
    page: Page,
    page_perms: PagePermissionTester,
    is_parent: Optional[bool] = False,
    next_url: Optional[str] = None,
) -> Button:
    yield Button(
        "Import",
        reverse("import_page", args=(page.id,)),
        priority=200,
        icon_name="upload",
    )
    yield Button(
        "Export",
        reverse("export_page", args=(page.id,)),
        priority=210,
        icon_name="download",
    )


def register_portable_page_admin_urls() -> List[URLPattern]:
    return [
        path("export/<int:page_id>/", export_view, name="export_page"),
        path("import/<int:page_id>/", import_view, name="import_page"),
    ]


hooks.register("register_page_listing_more_buttons")(page_listing_import_button)
hooks.register("register_admin_urls")(register_portable_page_admin_urls)
