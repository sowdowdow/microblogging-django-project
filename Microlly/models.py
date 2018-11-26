from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-creation_date",)
        verbose_name = "Publication"
        verbose_name_plural = "Publications"
