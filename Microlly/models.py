from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField()
    creation_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
