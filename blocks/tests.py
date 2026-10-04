from django.test import SimpleTestCase, TestCase
from wagtail import blocks
from wagtail.models import Site

from .cards import CardGridBlock
from .content import HeadingBlock
from .links import LinkBlock


class LinkBlockTests(TestCase):
    def test_external_url_sets_href(self):
        value = LinkBlock().to_python(
            {"text": "Example", "url": "https://example.com/", "page": None}
        )
        self.assertEqual(value.href, "https://example.com/")

    def test_text_without_destination_is_invalid(self):
        block = LinkBlock()
        value = block.to_python({"text": "Example", "url": "", "page": None})
        with self.assertRaises(blocks.StructBlockValidationError):
            block.clean(value)

    def test_page_and_url_together_are_invalid(self):
        block = LinkBlock()
        page = Site.objects.get(is_default_site=True).root_page.specific
        value = block.to_python(
            {"text": "Example", "url": "https://example.com/", "page": page.pk}
        )
        with self.assertRaises(blocks.StructBlockValidationError):
            block.clean(value)


class BlockValueTests(SimpleTestCase):
    def test_heading_generates_anchor(self):
        value = HeadingBlock().to_python(
            {"text": "Example Heading", "level": "h2", "visually_hidden": False}
        )
        self.assertEqual(value.anchor_id, "example-heading")

    def test_card_grid_uses_explicit_anchor(self):
        value = CardGridBlock().to_python(
            {
                "heading": "Example Grid",
                "anchor": "custom-anchor",
                "visually_hide_heading": False,
                "introduction": "",
                "cards": [],
            }
        )
        self.assertEqual(value.anchor_id, "custom-anchor")

    def test_card_grid_generates_anchor_from_heading(self):
        value = CardGridBlock().to_python(
            {
                "heading": "Example Grid",
                "anchor": "",
                "visually_hide_heading": False,
                "introduction": "",
                "cards": [],
            }
        )
        self.assertEqual(value.anchor_id, "example-grid")
