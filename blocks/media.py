from wagtail import blocks
from wagtail.images.blocks import ImageBlock


class ContentImageBlock(blocks.StructBlock):
    image = ImageBlock()
    caption = blocks.CharBlock(required=False, max_length=255)

    class Meta:
        template = "blocks/media/content_image.html"
        icon = "image"
        label = "Image"


class ScreenshotBlock(blocks.StructBlock):
    image = ImageBlock()
    caption = blocks.CharBlock(required=False, max_length=255)

    class Meta:
        template = "blocks/media/screenshot.html"
        icon = "image"
        label = "Screenshot"
