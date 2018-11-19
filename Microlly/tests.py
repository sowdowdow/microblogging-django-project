from django.test import TestCase
from django.urls import reverse
from django.db.models.query import QuerySet
from Microlly.models import Post


class WebsiteTestCase(TestCase):
    fixtures = ["initial.json"]

    def test_index_page(self):
        print("check nothing")
        #response = self.client.get(reverse("Microlly:index"))
        #self.assertContains(response, "posts")
        #self.assertEqual(type(response.context["posts"]), QuerySet)
        #self.failUnlessEqual(response.status_code, 200)
        #self.assertTemplateUsed("Post/index.html")

