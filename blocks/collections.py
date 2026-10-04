from .cards import CardBlock, CardGridBlock
from .content import HeadingBlock, NoteBlock, RichTextBlock
from .media import ContentImageBlock, ScreenshotBlock


CONTENT_BLOCKS = [
    ("heading", HeadingBlock()),
    ("richtext", RichTextBlock()),
    ("content_image", ContentImageBlock()),
    ("screenshot", ScreenshotBlock()),
    ("note", NoteBlock()),
]

CARD_BLOCKS = [
    ("card", CardBlock()),
    ("card_grid", CardGridBlock()),
]
