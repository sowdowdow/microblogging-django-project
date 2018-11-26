from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.views.defaults import page_not_found
from django.views.generic.edit import CreateView

from Microlly import forms
from Microlly.models import Post


def index(request):
    try:
        page = int(request.GET.get("page"))
    except:
        page = 1
    posts = Post.objects.all()
    paginator = Paginator(posts, 5)
    posts = paginator.page(page)
    return render(request, "index.html", {"posts": posts})


def post(request, id):
    post = get_object_or_404(Post, pk=id)
    return render(request, "post.html", {"post": post})


def login(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        redirect("Microlly:account")
    else:
        redirect("Microlly:login")


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("Microlly:login")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def account(request):
    user_posts = Post.objects.filter(author=request.user).all()
    isaccountview = True
    return render(
        request,
        "account.html",
        {"user_posts": user_posts, "isaccountview": isaccountview},
    )


@login_required
def createPost(request):
    if request.method == "POST":
        form = forms.PostCreateForm(request.POST or None)
        if form.is_valid():
            # not saved in DB
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect("Microlly:account")
        else:
            return render(request, "create_post.html", {"form": form})
    else:
        form = forms.PostCreateForm()
        return render(request, "create_post.html", {"form": form})


@login_required
def deletePost(request, id):
    post = get_object_or_404(Post, pk=id)
    if request.method == "POST":
        # suppress confirmed by user
        if post.author == request.user:
            post.delete()
            return render(request, "delete_post_done.html", {"post": post})
        else:
            redirect("Microlly:index")
    else:
        return render(request, "delete_post.html", {"id": id, "post": post})


@login_required
def editPost(request, id):
    post = get_object_or_404(Post, pk=id)
    if post.author != request.user:
        raise PermissionDenied
    if request.method == "POST":
        # check if is author of the post
        form = forms.PostCreateForm(request.POST or None)
        if form.is_valid():
            post.title = form.cleaned_data["title"]
            post.body = form.cleaned_data["body"]
            post.save()
            return redirect("Microlly:account")
        else:
            return render(request, "create_post.html", {"form": form})

    form = forms.PostEditForm(instance=post)
    return render(request, "edit_post.html", {"form": form})


def authorPosts(request, author):
    try:
        page = int(request.GET.get("page"))
    except:
        page = 1
    author = get_object_or_404(User, username=author)
    posts = get_list_or_404(Post, author=author)
    paginator = Paginator(posts, 5)
    posts = paginator.page(page)
    return render(request, "author_posts.html", {"posts": posts, "author": author})
