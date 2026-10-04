from django.core.exceptions import ValidationError
from wagtail import blocks


class LinkStructValue(blocks.StructValue):
    @property
    def href(self):
        if self.get("page"):
            return self["page"].url
        return self.get("url") or ""


class LinkBlock(blocks.StructBlock):
    text = blocks.CharBlock(required=False, max_length=100, label="Link text")
    page = blocks.PageChooserBlock(required=False, label="Internal page")
    url = blocks.URLBlock(required=False, label="External URL")

    def clean(self, value):
        result = super().clean(value)
        page = result.get("page")
        url = result.get("url")
        if not page and not url and result.get("text"):
            raise blocks.StructBlockValidationError(non_block_errors=ValidationError("Choose an internal page or enter an external URL."))
        if page and url:
            raise blocks.StructBlockValidationError(non_block_errors=ValidationError("Choose either an internal page or an external URL, not both."))
        return result

    class Meta:
        value_class = LinkStructValue
        icon = "link"
        label = "Link"
