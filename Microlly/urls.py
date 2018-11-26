from django.urls import path, include
from Microlly import views

app_name = "Microlly"


urlpatterns = [
    path("", views.index, name="index"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('account/', views.account, name="account"),
    path('accounts/signup/', views.signup, name='signup'),
    path('post/<int:id>/', views.post, name="post"),
    path('create-post/', views.createPost, name="create_post"),
    path('edit-post/<int:id>/', views.editPost, name="edit_post"),
    path('delete-post/<int:id>/', views.deletePost, name="delete_post"),
    path('<slug:author>/posts/', views.authorPosts, name="author_posts"),
]
