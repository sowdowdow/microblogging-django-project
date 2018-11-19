from django.test import TestCase
from django.urls import reverse
from django.db.models.query import QuerySet
from Microlly.models import Post


class WebsiteTestCase(TestCase):
    fixtures = ["initial.json"]

    def test_index_page(self):
        # getting the wanted page
        response = self.client.get(reverse("Microlly:index"))
        # This one check for text in the rendered html
        self.assertContains(response, "Liste des dernières publications")
        self.assertEqual(type(response.context["posts"]), QuerySet)
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed("Post/index.html")

