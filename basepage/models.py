from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.images import get_image_model_string
from wagtail.models import AbstractPage, DefaultBasePageMixin
from wagtail.search import index


class BasePage(DefaultBasePageMixin, AbstractPage):
    search_fields = [
        index.SearchField("title", boost=2),
        index.AutocompleteField("title"),
        index.FilterField("title"),
        index.FilterField("id"),
        index.FilterField("live"),
        index.FilterField("owner"),
        index.FilterField("content_type"),
        index.FilterField("path"),
        index.FilterField("depth"),
        index.FilterField("locked"),
        index.FilterField("first_published_at"),
        index.FilterField("last_published_at"),
        index.FilterField("latest_revision_created_at"),
        index.FilterField("locale"),
        index.FilterField("translation_key"),
        index.FilterField("show_in_menus"),
    ]

    social_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Image used when this page is shared on social media.",
    )

    canonical_url = models.URLField(
        blank=True,
        help_text="Optional canonical URL override.",
    )

    robots_noindex = models.BooleanField(
        default=False,
        help_text="Ask search engines not to index this page.",
    )

    promote_panels = DefaultBasePageMixin.promote_panels + [
        FieldPanel("social_image"),
        FieldPanel("canonical_url"),
        FieldPanel("robots_noindex"),
    ]
