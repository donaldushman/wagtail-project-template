from django.utils.text import slugify
from wagtail import blocks

from .links import LinkBlock


class HeadingStructValue(blocks.StructValue):
    @property
    def anchor_id(self):
        return slugify(self.get("text", ""))


class HeadingBlock(blocks.StructBlock):
    text = blocks.CharBlock(required=True, help_text="Heading text")
    level = blocks.ChoiceBlock(choices=[("h2","Heading 2"),("h3","Heading 3"),("h4","Heading 4"),("h5","Heading 5"),("h6","Heading 6")], default="h2", help_text="Choose the heading level that fits the page structure.")
    visually_hidden = blocks.BooleanBlock(required=False, default=False, label="Visually hide heading")

    class Meta:
        template = "blocks/content/heading.html"
        value_class = HeadingStructValue
        icon = "title"
        label = "Heading"


class RichTextBlock(blocks.RichTextBlock):
    def __init__(self, **kwargs):
        kwargs.setdefault("features", ["bold", "italic", "ol", "ul", "hr", "link"])
        super().__init__(**kwargs)

    class Meta:
        template = "blocks/content/rich_text.html"
        icon = "doc-full"
        label = "Rich text"


class NoteBlock(blocks.StructBlock):
    text = blocks.TextBlock()
    link = LinkBlock(required=False, label="Link")

    class Meta:
        template = "blocks/content/note.html"
        icon = "info-circle"
        label = "Note"
