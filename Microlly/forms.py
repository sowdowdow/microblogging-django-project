from django import forms
from Microlly import models

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = [
            'title',
            'body',
        ]