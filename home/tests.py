from django.test import TestCase
from wagtail.models import Site

from .models import HomePage


class HomePageTests(TestCase):
    def test_default_site_uses_homepage(self):
        site = Site.objects.get(is_default_site=True)
        self.assertIsInstance(site.root_page.specific, HomePage)

    def test_homepage_renders(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Home")
