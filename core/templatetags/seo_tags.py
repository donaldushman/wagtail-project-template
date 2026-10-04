from django import template
from wagtail.models import AbstractPage, Site

from core.models import SEOSettings

register = template.Library()


def absolute_url(request, url):
    if not url:
        return ""
    if url.startswith(("http://", "https://")):
        return url
    if request:
        return request.build_absolute_uri(url)
    return ""


@register.inclusion_tag("core/seo/meta.html", takes_context=True)
def seo_meta(context, page=None, title=None, description="", noindex=False):
    request = context.get("request")
    site = Site.find_for_request(request) if request else None
    seo_settings = SEOSettings.load(request_or_site=request) if request else None

    if isinstance(page, AbstractPage):
        title = page.seo_title or page.title
        description = page.search_description
        canonical_url = page.canonical_url
        if not canonical_url and request:
            canonical_url = page.get_full_url(request)
        social_image = page.social_image or (
            seo_settings.default_social_image if seo_settings else None
        )
        noindex = page.robots_noindex
    else:
        canonical_url = request.build_absolute_uri(request.path) if request else ""
        social_image = seo_settings.default_social_image if seo_settings else None

    social_image_url = ""
    if social_image:
        rendition = social_image.get_rendition("fill-1200x630|format-webp")
        social_image_url = absolute_url(request, rendition.url)

    return {
        "title": title,
        "site_name": site.site_name if site else "",
        "description": description,
        "canonical_url": canonical_url,
        "social_image_url": social_image_url,
        "noindex": noindex,
    }
