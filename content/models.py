from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.search import index

from basepage.models import BasePage
from blocks.collections import CARD_BLOCKS, CONTENT_BLOCKS


class ContentPage(BasePage):
    body = StreamField(CONTENT_BLOCKS + CARD_BLOCKS, blank=True)

    search_fields = BasePage.search_fields + [index.SearchField("body")]
    content_panels = BasePage.content_panels + [FieldPanel("body")]
