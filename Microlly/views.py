from django.shortcuts import render
from Microlly.models import Post
from Microlly import forms
from django.contrib.auth.models import User

def index(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {'posts': posts})

def signup(request):
    if request.method != 'POST':
        return render(request, 'registration/signup.html', {'form': forms.SignupForm})
    else:
        posts = request.post()
        if posts:
            return render(request, 'registration/signup.html', {'posts': posts})
