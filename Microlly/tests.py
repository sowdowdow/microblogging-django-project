from django.contrib.auth.models import User
from django.core.paginator import Page
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.http.response import JsonResponse, HttpResponseRedirect
from django.test import Client, TestCase
from django.urls import reverse

from Microlly.models import Comment, Post


class WebsiteTestCase(TestCase):
    fixtures = ["initial.json"]

    def test_index_page(self):
        response = self.client.get(reverse("Microlly:index"))
        self.assertContains(response, "Les dernières news")
        self.assertEqual(type(response.context["posts"]), Page)
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_login_page(self):
        response = self.client.get(reverse("Microlly:login"))
        self.assertContains(response, "Connexion")
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_login_page_success(self):
        response = self.client.post(
            reverse("Microlly:login"),
            {"username": "gerard", "password": "motdepasse123"},
            follow=True,
        )
        self.assertContains(response, "Mon Compte")
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account.html")

    def test_login_page_fail(self):
        response = self.client.post(
            reverse("Microlly:login"),
            {"username": "gerard", "password": "mauvaismotdepasse"},
        )
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_signup_page(self):
        response = self.client.get(reverse("Microlly:signup"))
        self.assertContains(response, "Créer un compte")
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_account_page_success(self):
        # logged in test
        self.client.login(username="gerard", password="motdepasse123")
        response = self.client.get(reverse("Microlly:account"))
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account.html")

    def test_account_page_failure(self):
        # logged out test
        response = self.client.get(reverse("Microlly:account"))
        self.failUnlessEqual(response.status_code, 302)

    def test_create_post_page_success(self):
        self.client.login(username="gerard", password="motdepasse123")
        response = self.client.get(reverse("Microlly:create_post"))
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "create_post.html")

    def test_create_post_page_failure(self):
        # logged out test
        response = self.client.get(reverse("Microlly:create_post"))
        self.failUnlessEqual(response.status_code, 302)

    def test_delete_post_page_success(self):
        self.client.login(username="gerard", password="motdepasse123")
        user = User.objects.get(username="gerard")
        user_post = Post.objects.filter(author=user).first()
        response = self.client.get(
            reverse("Microlly:delete_post", kwargs={"id": user_post.id})
        )
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "delete_post.html")

    def test_delete_post_page_fail(self):
        # logged out test
        response = self.client.get(reverse("Microlly:delete_post", kwargs={"id": 1}))
        self.failUnlessEqual(response.status_code, 302)

    def test_delete_post_done_page(self):
        self.client.login(username="gerard", password="motdepasse123")
        user = User.objects.get(username="gerard")
        user_post = Post.objects.filter(author=user).first()
        response = self.client.post(
            reverse("Microlly:delete_post", kwargs={"id": user_post.id})
        )
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "delete_post_done.html")

    def test_post_page_success(self):
        # Specific post page
        tmp_user = User.objects.get(username="gerard")
        tmp_post = Post.objects.filter(author=tmp_user).first()
        response = self.client.get(reverse("Microlly:post", kwargs={"id": tmp_post.id}))
        self.assertContains(response, tmp_post.title)
        self.assertContains(response, tmp_post.body)
        self.assertEqual(type(response.context["post"]), Post)
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed("post.html")

    def test_post_page_failed(self):
        # specific invalid post page
        response = self.client.get(reverse("Microlly:post", kwargs={"id": 99999}))
        self.failUnlessEqual(response.status_code, 404)
        self.assertTemplateUsed("404.html")

    def test_edit_page_success(self):
        # test a possible post editing
        tmp_user = User.objects.get(username="gerard")
        tmp_post = Post.objects.filter(author=tmp_user).first()
        self.client.login(username="gerard", password="motdepasse123")
        response = self.client.get(
            reverse("Microlly:edit_post", kwargs={"id": tmp_post.id})
        )
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_post.html")

    def test_edit_page_forbidden(self):
        # impossible edit test
        self.client.login(username="gerard", password="motdepasse123")
        tmp_user = User.objects.get(username="marie")
        post_id_not_from_user = Post.objects.filter(author=tmp_user).first().id
        response = self.client.get(
            reverse("Microlly:edit_post", kwargs={"id": post_id_not_from_user})
        )
        self.failUnlessEqual(response.status_code, 403)
        self.assertTemplateUsed("403.html")

    def test_edit_page_unlogged(self):
        # logged out test
        post_id = Post.objects.get(pk=1).id
        response = self.client.get(
            reverse("Microlly:edit_post", kwargs={"id": post_id})
        )
        self.failUnlessEqual(response.status_code, 302)

    def test_author_posts_page(self):
        author = User.objects.get(pk=1)
        response = self.client.get(
            reverse("Microlly:author_posts", kwargs={"author": author})
        )
        self.assertContains(response, "Les publications de <b>" + str(author) + "</b>")
        self.assertEqual(type(response.context["posts"]), Page)
        self.assertTemplateUsed(response, "author_posts.html")
        self.failUnlessEqual(response.status_code, 200)

    def test_password_reset(self):
        response = self.client.get(reverse("Microlly:password_reset"))
        self.assertContains(response, "Réinitialisation du mot de passe")
        self.assertTemplateUsed(response, "registration/password_reset_form.html")
        self.failUnlessEqual(response.status_code, 200)

    def test_password_change_fail(self):
        response = self.client.get(reverse("Microlly:password_change"))
        self.failUnlessEqual(response.status_code, 302)

    def test_password_change_success(self):
        self.client.login(username="gerard", password="motdepasse123")
        response = self.client.get(reverse("Microlly:password_change"))
        self.assertContains(response, "Modification du mot de passe")
        self.assertTemplateUsed(response, "registration/password_change_form.html")
        self.failUnlessEqual(response.status_code, 200)

    def test_password_change_done(self):
        self.client.login(username="gerard", password="motdepasse123")
        response = self.client.post(
            reverse("Microlly:password_change"),
            {
                "old_password": "motdepasse123",
                "new_password1": "unsupermotdepasse",
                "new_password2": "unsupermotdepasse",
            },
            # follow redirection, useful to check template later
            follow=True,
        )
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/password_change_done.html")

    # try to create a comment unconnected
    def test_comment_create_fail(self):
        response = self.client.post(reverse("Microlly:comment_create"))
        self.failUnlessEqual(response.status_code, 302)

    # create a comment
    def test_comment_create_sucess(self):
        self.client.login(username="gerard", password="motdepasse123")
        response = self.client.post(
            reverse("Microlly:comment_create"),
            {"message": "Content of the comment bla bla bla.", "post": 1},
            follow=True,
        )
        self.failUnlessEqual(response.status_code, 200)
        self.assertEqual(type(response), HttpResponse)
        self.assertTemplateUsed(response, "post.html")

    # try to read a non existing comment
    def test_comment_read_fail(self):
        response = self.client.get(
            reverse("Microlly:comment_read", kwargs={"id": 999999})
        )
        self.failUnlessEqual(response.status_code, 404)

    def test_comment_read_sucess(self):
        response = self.client.get(reverse("Microlly:comment_read", kwargs={"id": 1}))
        self.failUnlessEqual(response.status_code, 200)
        self.assertEqual(type(response), JsonResponse)

    def test_comment_update_fail_unconnected(self):
        response = self.client.patch(
            reverse("Microlly:comment_update", kwargs={"id": 1})
        )
        self.failUnlessEqual(response.status_code, 302)

    def test_comment_update_fail_not_owner(self):
        self.client.login(username="gerard", password="motdepasse123")
        response = self.client.patch(
            reverse(
                "Microlly:comment_update",
                kwargs={"id": 1},  # 1st comment is not from gerard
            ),
            {"message": "updated message, but failing"},
        )
        self.failUnlessEqual(response.status_code, 302)  # this is to fix -> 403

    def test_comment_update_sucess(self):
        self.client.login(username="gerard", password="motdepasse123")
        user = User.objects.get(username="gerard")
        user_comment = Post.objects.filter(author=user).first()
        response = self.client.patch(
            reverse("Microlly:comment_update", kwargs={"id": user_comment.id}),
            {"message": "updated message success"},
        )
        self.failUnlessEqual(response.status_code, 302)
        self.assertEqual(type(response), HttpResponseRedirect)

    def test_comment_delete_fail_not_owner(self):
        self.client.login(username="gerard", password="motdepasse123")
        response = self.client.delete(
            reverse(
                "Microlly:comment_delete",
                kwargs={"id": 1},  # gerard is not owner of comment 1
            )
        )
        self.failUnlessEqual(response.status_code, 302)  # this is to fix -> 403

    def test_comment_delete_fail_unconnected(self):
        response = self.client.delete(
            reverse("Microlly:comment_delete", kwargs={"id": 1})
        )
        self.failUnlessEqual(response.status_code, 302)

    def test_comment_delete_sucess(self):
        self.client.login(username="gerard", password="motdepasse123")
        response = self.client.delete(
            reverse(
                "Microlly:comment_delete", kwargs={"id": 2}  # id of gerard's comment
            )
        )
        self.failUnlessEqual(response.status_code, 302)

    def test_like_post_fail(self):
        # fail because not connected
        response = self.client.get(
            reverse(
                "Microlly:post_like", kwargs={"id": 1}
            )
        )
        self.failUnlessEqual(response.status_code, 302)
        self.assertEqual(type(response), HttpResponseRedirect)

    def test_like_post_success(self):
        self.client.login(username="gerard", password="motdepasse123")
        response = self.client.get(
            reverse(
                "Microlly:post_like", kwargs={"id": 1}
            ),
            follow=True
        )
        self.failUnlessEqual(response.status_code, 200)
        self.assertEqual(type(response), HttpResponse)
