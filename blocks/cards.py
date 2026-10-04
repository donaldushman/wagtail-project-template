from django.utils.text import slugify
from wagtail import blocks
from wagtail.images.blocks import ImageBlock

from .content import RichTextBlock
from .links import LinkBlock


class CardBlock(blocks.StructBlock):
    image = ImageBlock(required=False)
    title = blocks.CharBlock(required=True, max_length=100)
    content = blocks.RichTextBlock(required=False, features=["bold", "italic", "link"])
    link = LinkBlock(required=False)

    class Meta:
        template = "blocks/cards/card.html"
        icon = "doc-empty"
        label = "Card"


class CardGridStructValue(blocks.StructValue):
    @property
    def anchor_id(self):
        return slugify(self.get("anchor") or self.get("heading", ""))


class CardGridBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=True, max_length=255)
    anchor = blocks.CharBlock(required=False, help_text="Optional URL anchor. Leave blank to generate one from the heading.")
    visually_hide_heading = blocks.BooleanBlock(required=False, default=False, label="Visually hide heading")
    introduction = RichTextBlock(required=False)
    cards = blocks.ListBlock(CardBlock(), min_num=1)

    class Meta:
        template = "blocks/cards/card_grid.html"
        value_class = CardGridStructValue
        icon = "grip"
        label = "Card grid"
