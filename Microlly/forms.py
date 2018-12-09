from django import forms
from Microlly import models


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ["title", "body"]


class PostEditForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ["id", "title", "body"]


class CommentCreateForm(forms.ModelForm):
    message = forms.CharField(
        required=True, min_length=10, max_length=250, label="", widget=forms.Textarea(
            attrs={
                "class": "textarea is-link",
                "placeholder": "Laisser un commentaire",
                "rows": 3,
            }
        )
    )

    class Meta:
        model = models.Comment
        fields = ["message"]

