from django.http import HttpResponse
from django.test import RequestFactory, TestCase, override_settings
from wagtail.models import Site

from content.models import ContentPage
from core.middleware import CanonicalHostMiddleware
from core.templatetags.menu_tags import menu_page_state
from core.templatetags.seo_tags import seo_meta


class CorePageTestCase(TestCase):
    def setUp(self):
        self.site = Site.objects.get(is_default_site=True)
        self.home = self.site.root_page.specific
        self.page = ContentPage(
            title="Example Page",
            slug="example-page",
            show_in_menus=True,
            search_description="Example description",
        )
        self.home.add_child(instance=self.page)
        self.page.save_revision().publish()


class NavigationTests(CorePageTestCase):
    def test_current_page_state(self):
        self.assertEqual(menu_page_state({"page": self.page}, self.page), "current")

    def test_ancestor_page_state(self):
        child = ContentPage(title="Child", slug="child")
        self.page.add_child(instance=child)
        self.assertEqual(menu_page_state({"page": child}, self.page), "ancestor")

    def test_unrelated_page_state(self):
        other = ContentPage(title="Other", slug="other")
        self.home.add_child(instance=other)
        self.assertEqual(menu_page_state({"page": other}, self.page), "")


class SearchTests(CorePageTestCase):
    def test_search_page_renders_without_query(self):
        response = self.client.get("/search/")
        self.assertEqual(response.status_code, 200)

    def test_search_finds_published_page(self):
        response = self.client.get("/search/", {"query": "Example"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Example Page")

    def test_search_handles_no_results(self):
        response = self.client.get("/search/", {"query": "NoSuchPhrase"})
        self.assertContains(response, "No results found.")


class SEOTests(CorePageTestCase):
    def test_page_seo_values(self):
        request = RequestFactory().get("/example-page/", HTTP_HOST="localhost")
        result = seo_meta({"request": request}, page=self.page)
        self.assertEqual(result["title"], "Example Page")
        self.assertEqual(result["description"], "Example description")
        self.assertFalse(result["noindex"])
        self.assertTrue(result["canonical_url"].endswith("/example-page/"))

    def test_canonical_override_and_noindex(self):
        self.page.canonical_url = "https://example.com/canonical/"
        self.page.robots_noindex = True
        request = RequestFactory().get("/example-page/", HTTP_HOST="localhost")
        result = seo_meta({"request": request}, page=self.page)
        self.assertEqual(result["canonical_url"], "https://example.com/canonical/")
        self.assertTrue(result["noindex"])


class CanonicalHostMiddlewareTests(TestCase):
    @override_settings(SITE_URL="https://example.com", ALLOWED_HOSTS=["example.com", "www.example.com"])
    def test_www_redirects_to_canonical_host(self):
        middleware = CanonicalHostMiddleware(lambda request: HttpResponse("ok"))
        request = RequestFactory().get(
            "/example/?a=1", HTTP_HOST="www.example.com"
        )
        response = middleware(request)
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"], "https://example.com/example/?a=1")

    @override_settings(SITE_URL="https://example.com", ALLOWED_HOSTS=["example.com", "www.example.com"])
    def test_canonical_host_is_not_redirected(self):
        middleware = CanonicalHostMiddleware(lambda request: HttpResponse("ok"))
        request = RequestFactory().get("/example/", HTTP_HOST="example.com")
        response = middleware(request)
        self.assertEqual(response.status_code, 200)
