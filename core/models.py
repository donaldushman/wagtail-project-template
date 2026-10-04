from django.db import models
from wagtail.contrib.settings.models import BaseGenericSetting, BaseSiteSetting, register_setting
from wagtail.images import get_image_model_string


@register_setting
class SiteSettings(BaseSiteSetting):
    logo = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Optional site logo displayed in the header.",
    )


@register_setting
class SEOSettings(BaseGenericSetting):
    organization_name = models.CharField(max_length=255, blank=True)
    default_social_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Default image used when a page does not define its own social image.",
    )
