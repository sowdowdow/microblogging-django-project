from django.contrib.auth import views as auth_views
from django.urls import include, path, reverse_lazy

from Microlly import views

app_name = "Microlly"


urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/", views.account, name="account"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/signup/", views.signup, name="signup"),
    path(
        "accounts/password-change/",
        auth_views.PasswordChangeView.as_view(
            success_url=reverse_lazy("Microlly:password_change_done")
        ),
        name="password_change",
    ),
    path(
        "accounts/password-change/done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("post/<int:id>/", views.post, name="post"),
    path("create-post/", views.createPost, name="create_post"),
    path("edit-post/<int:id>/", views.editPost, name="edit_post"),
    path("delete-post/<int:id>/", views.deletePost, name="delete_post"),
    path("<slug:author>/posts/", views.authorPosts, name="author_posts"),
    # Comments
    path("comment/create/", views.commentCreate, name="comment_create"),
    path("comment/read/<int:id>/", views.commentRead, name="comment_read"),
    path("comment/update/<int:id>/", views.commentUpdate, name="comment_update"),
    path("comment/delete/<int:id>/", views.commentDelete, name="comment_delete"),
]
