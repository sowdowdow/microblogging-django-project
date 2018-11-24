from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.test import Client, TestCase
from django.urls import reverse

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

    def test_signup_page(self):
        response = self.client.get(reverse("Microlly:signup"))
        self.assertContains(response, "Créer un compte")
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_account_page(self):
        self.client.force_login(
            User.objects.create_user(username="temporary", password="temporary")
        )
        response = self.client.get(reverse("Microlly:account"))
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account.html")
        # logged out test
        self.client.logout()
        response = self.client.get(reverse("Microlly:account"))
        self.failUnlessEqual(response.status_code, 302)

    def test_create_post_page(self):
        self.client.force_login(
            User.objects.create_user(username="temporary", password="temporary")
        )
        response = self.client.get(reverse("Microlly:create_post"))
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "create_post.html")