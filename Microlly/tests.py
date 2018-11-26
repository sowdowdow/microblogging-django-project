from django.contrib.auth.models import User
from django.core.paginator import Page
from django.db.models.query import QuerySet
from django.test import Client, TestCase
from django.urls import reverse

from Microlly.models import Post


class WebsiteTestCase(TestCase):
    fixtures = ["initial.json"]

    def test_index_page(self):
        response = self.client.get(reverse("Microlly:index"))
        self.assertContains(response, "Liste des dernières publications")
        self.assertEqual(type(response.context["posts"]), Page)
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
        # logged out test
        self.client.logout()
        response = self.client.get(reverse("Microlly:create_post"))
        self.failUnlessEqual(response.status_code, 302)

    def test_delete_post_page(self):
        tmp_user = User.objects.create_user(username="temporary", password="temporary")
        self.client.force_login(tmp_user)
        tmp_post = Post.objects.create(
            title="temporary", body="temporary", author=tmp_user
        )
        response = self.client.get(
            reverse("Microlly:delete_post", kwargs={"id": tmp_post.id})
        )
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "delete_post.html")
        # logged out test
        self.client.logout()
        response = self.client.get(
            reverse("Microlly:delete_post", kwargs={"id": tmp_post.id})
        )
        self.failUnlessEqual(response.status_code, 302)

    def test_delete_post_done_page(self):
        tmp_user = User.objects.create_user(username="temporary", password="temporary")
        self.client.force_login(tmp_user)
        tmp_post = Post.objects.create(
            title="temporary", body="temporary", author=tmp_user
        )
        response = self.client.post(
            reverse("Microlly:delete_post", kwargs={"id": tmp_post.id})
        )
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "delete_post_done.html")

    def test_post_page(self):
        # Specific post page
        tmp_user = User.objects.create_user(username="temporary", password="temporary")
        tmp_post = Post.objects.create(
            title="temporary", body="temporary", author=tmp_user
        )
        response = self.client.get(reverse("Microlly:post", kwargs={"id": tmp_post.id}))
        self.assertContains(response, tmp_post.title)
        self.assertContains(response, tmp_post.body)
        self.assertEqual(type(response.context["post"]), Post)
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed("post.html")
        impossible_id = User.objects.last().id + 1
        response = self.client.get(
            reverse("Microlly:post", kwargs={"id": impossible_id})
        )
        self.failUnlessEqual(response.status_code, 404)
        self.assertTemplateUsed("404.html")

    def test_edit_page(self):
        tmp_user = User.objects.create_user(username="temporary", password="temporary")
        tmp_post = Post.objects.create(
            title="temporary", body="temporary", author=tmp_user
        )
        self.client.force_login(tmp_user)
        response = self.client.get(
            reverse("Microlly:edit_post", kwargs={"id": tmp_post.id})
        )
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_post.html")
        # impossible edit test
        impossible_id = User.objects.last().id + 1
        response = self.client.get(
            reverse("Microlly:post", kwargs={"id": impossible_id})
        )
        self.failUnlessEqual(response.status_code, 404)
        self.assertTemplateUsed("404.html")
        # logged out test
        self.client.logout()
        response = self.client.get(
            reverse("Microlly:edit_post", kwargs={"id": tmp_post.id})
        )
        self.failUnlessEqual(response.status_code, 302)

    def test_author_posts_page(self):
        tmp_user = User.objects.create_user(username="temporary", password="temporary")
        tmp_post = Post.objects.create(
            title="temporary", body="temporary", author=tmp_user
        )
        response = self.client.get(
            reverse("Microlly:author_posts", kwargs={"author": tmp_user})
        )
        self.assertContains(
            response, "Les publications de <b>" + str(tmp_user) + "</b>"
        )
        self.assertEqual(type(response.context["posts"]), Page)
        self.assertTemplateUsed(response, "author_posts.html")
        self.failUnlessEqual(response.status_code, 200)
