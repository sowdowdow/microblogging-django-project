from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.views.defaults import page_not_found
from django.views.generic.edit import CreateView

from Microlly import forms, ranking
from Microlly.models import Comment, Post


# the index listing all the posts
def index(request):
    try:
        page = int(request.GET.get("page"))
    except:
        page = 1
    posts = Post.objects.all()
    paginator = Paginator(posts, 5)
    posts = paginator.page(page)
    return render(request, "index.html", {"posts": posts})


# unique view of a post
def post(request, id):
    post = get_object_or_404(Post, pk=id)
    comments = Comment.objects.filter(post=post)
    comment_form = forms.CommentCreateForm()
    return render(
        request, "post.html", {"post": post, "form": comment_form, "comments": comments}
    )


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
    number_of_posts = len(user_posts)
    user_rank = ranking.get_rank(number_of_posts)
    isaccountview = True
    return render(
        request,
        "account.html",
        {
            "user_posts": user_posts,
            "isaccountview": isaccountview,
            "number_of_user_posts": number_of_posts,
            "rank": user_rank,
        },
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
        # cancel case by user
        if "cancel" in request.POST:
            return redirect("Microlly:account")
        # suppress confirmed by user
        if post.author == request.user:
            post.delete()
            return render(request, "delete_post_done.html", {"post": post})
        else:
            raise PermissionDenied
    else:
        return render(request, "delete_post.html", {"id": id, "post": post})


@login_required
def editPost(request, id):
    post = get_object_or_404(Post, pk=id)
    # check if is author of the post
    if post.author != request.user:
        raise PermissionDenied
    if request.method == "POST":
        # post was edited and is saved
        form = forms.PostCreateForm(request.POST or None)
        if form.is_valid():
            post.title = form.cleaned_data["title"]
            post.body = form.cleaned_data["body"]
            post.save()
            return redirect("Microlly:account")
        else:
            return render(request, "create_post.html", {"form": form})
    # pre-edition of the post
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


@login_required
def commentCreate(request):
    if request.method != "POST":
        return JsonResponse({"error": "expected POST method"})

    comment_form = forms.CommentCreateForm(request.POST or None)

    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.author = request.user
        new_comment.post = Post.objects.get(pk=request.POST["post"])
        new_comment.save()
        return redirect("Microlly:post", id=request.POST["post"])
    else:
        return JsonResponse({"error": "saving failed"})


def commentRead(request, id):
    comment = get_object_or_404(Comment, pk=id)
    return JsonResponse(model_to_dict(comment))


@login_required
def commentUpdate(request, id):
    comment = get_object_or_404(Comment, pk=id)
    post_id = Post.objects.get(title=comment.post).id
    if comment.author != request.user:
        raise PermissionDenied
    # TODO
    # create the modify comment view or what else ?
    return redirect("Microlly:post", id=post_id)


@login_required
def commentDelete(request, id):
    comment = get_object_or_404(Comment, pk=id)
    if comment.author != request.user:
        raise PermissionDenied
    comment.delete()
    return redirect("Microlly:post", id=comment.post.id)

