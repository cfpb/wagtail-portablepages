from __future__ import annotations

import json

from django.test import TestCase

from wagtail.models import Site
from wagtail.test.testapp.models import StreamPage

from portablepages.utils import (
    export_page,
    get_last_migration,
    import_page,
)


class LastMigrationTestCase(TestCase):
    def test_get_last_migration_has_migrations(self):
        app_label = StreamPage._meta.app_label
        last_migration = get_last_migration(app_label)
        self.assertNotEqual(last_migration, "")

    def test_get_last_migration_no_migrations(self):
        last_migration = get_last_migration("nonexistent")
        self.assertEqual(last_migration, "")


class ExportPageTestCase(TestCase):
    def setUp(self):
        self.page = StreamPage(
            title="Test page",
            slug="test-page",
            body=[("text", "Hello, world!")],
            live=True,
        )

    def test_export_page(self):
        page_json = export_page(self.page)

        page_data = json.loads(page_json)

        self.assertEqual(page_data["app_label"], "tests")
        self.assertEqual(page_data["model"], "streampage")
        self.assertEqual(page_data["data"]["title"], self.page.title)
        self.assertEqual(page_data["data"]["slug"], self.page.slug)

        self.assertListEqual(
            json.loads(page_data["data"]["body"]),
            list(self.page.body.raw_data),
        )


class ImportPageTestCase(TestCase):
    def setUp(self):
        self.root_page = Site.objects.get(is_default_site=True).root_page
        self.original_page = StreamPage(
            title="Test page",
            slug="test-page",
            body=[("text", "Hello, world!")],
            live=True,
        )
        self.page_json = export_page(self.original_page)

    def test_import_page_model_does_not_exist(self):
        page_json = json.dumps(
            {
                "app_label": "tests",
                "model": "PageModelDoesNotExist",
                "last_migration": "",
                "data": {},
            }
        )
        with self.assertRaises(LookupError), self.assertLogs(
            "portablepages"
        ) as cm:
            import_page(self.root_page, page_json)

        self.assertEqual(len(cm.output), 1)
        self.assertIn("Unable to import page of type", cm.output[0])

    def test_import_page_app_does_not_exist(self):
        page_json = json.dumps(
            {
                "app_label": "app_does_not_exist",
                "model": "streampage",
                "last_migration": "",
                "data": {},
            }
        )
        with self.assertRaises(LookupError), self.assertLogs(
            "portablepages"
        ) as cm:
            import_page(self.root_page, page_json)

        self.assertEqual(len(cm.output), 1)
        self.assertIn("Unable to import page of type", cm.output[0])

    def test_import_page_mismatched_migrations(self):
        page_json = json.dumps(
            {
                "app_label": "tests",
                "model": "streampage",
                "last_migration": "XXXX_non_existent_migration",
                "data": {},
            }
        )
        with self.assertRaises(ValueError), self.assertLogs(
            "portablepages"
        ) as cm:
            import_page(self.root_page, page_json)

        self.assertEqual(len(cm.output), 1)
        self.assertIn("Mismatched migrations", cm.output[0])

    def test_import_page(self):
        page = import_page(self.root_page, self.page_json)

        self.assertEqual(page.title, self.original_page.title)
        self.assertEqual(page.slug, self.original_page.slug)
        self.assertEqual(page.body, self.original_page.body)
