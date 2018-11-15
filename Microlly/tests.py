from django.test import TestCase
from django.urls import reverse
from django.db.models.query import QuerySet
from Microlly.models import Post


class WebsiteTestCase(TestCase):
    fixtures = ["initial.json"]

    def test_index_page(self):
        response = self.client.get(reverse("Microlly:index"))
        self.assertContains(response, "posts")
        self.assertEqual(type(response.context["posts"]), QuerySet)
        self.assertEqual(len(response.context["posts"]), 3)
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed("Post/index.html")

