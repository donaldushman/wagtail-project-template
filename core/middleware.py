from urllib.parse import urlparse

from django.conf import settings
from django.http import HttpResponsePermanentRedirect


class CanonicalHostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.canonical_host = urlparse(settings.SITE_URL).hostname

    def __call__(self, request):
        host = request.get_host().split(":")[0]
        if self.canonical_host and host == f"www.{self.canonical_host}":
            return HttpResponsePermanentRedirect(
                f"{settings.SITE_URL.rstrip('/')}{request.get_full_path()}"
            )
        return self.get_response(request)
