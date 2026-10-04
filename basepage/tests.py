from django.test import TestCase
from wagtail.search import index

from .models import BasePage


class BasePageTests(TestCase):
    def test_seo_fields_have_safe_defaults(self):
        page = BasePage(title="Example")
        self.assertEqual(page.canonical_url, "")
        self.assertFalse(page.robots_noindex)
        self.assertIsNone(page.social_image)

    def test_title_is_searchable_and_autocompletable(self):
        title_fields = [
            field for field in BasePage.search_fields if field.field_name == "title"
        ]
        self.assertTrue(any(isinstance(field, index.SearchField) for field in title_fields))
        self.assertTrue(any(isinstance(field, index.AutocompleteField) for field in title_fields))
