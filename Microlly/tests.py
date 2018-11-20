from django.test import TestCase
from django.urls import reverse
from django.db.models.query import QuerySet
from Microlly.models import Post


class WebsiteTestCase(TestCase):
    fixtures = ["initial.json"]

    def test_index_page(self):
        response = self.client.get(reverse("Microlly:index"))
        self.assertContains(response, "Liste des dernières publications")
        self.assertEqual(type(response.context["posts"]), QuerySet)
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
    
    def test_login_page(self):
        response = self.client.get(reverse("Microlly:login"))
        self.assertContains(response, "Connexion")
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

