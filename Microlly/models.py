from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=150)
    body = RichTextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-id",)
        verbose_name = "Publication"
        verbose_name_plural = "Publications"


class Comment(models.Model):
    message = models.CharField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    creation_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    def __str__(self):
        if len(self.message) <= 10:
            return self.message
        else:
            return self.message[:10]+"..."

    class Meta:
        ordering = ("-id",)
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
