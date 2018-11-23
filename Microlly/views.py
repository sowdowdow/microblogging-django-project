from django.shortcuts import render
from Microlly.models import Post
from django.contrib.auth.models import User

def index(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {'posts': posts})

def signup(request):
    return render(request, 'registration/signup.html')