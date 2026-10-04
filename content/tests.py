from django.test import TestCase
from wagtail.models import Site

from blocks.collections import CARD_BLOCKS, CONTENT_BLOCKS
from home.models import HomePage
from .models import ContentPage


class ContentPageTests(TestCase):
    def setUp(self):
        self.home = Site.objects.get(is_default_site=True).root_page.specific

    def test_expected_blocks_are_available(self):
        block_names = [name for name, block in CONTENT_BLOCKS + CARD_BLOCKS]
        self.assertEqual(
            block_names,
            ["heading", "richtext", "content_image", "note", "card", "card_grid"],
        )

    def test_content_page_can_be_created_and_rendered(self):
        page = ContentPage(title="Test Page", slug="test-page")
        self.home.add_child(instance=page)
        page.save_revision().publish()

        response = self.client.get(page.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Page")
