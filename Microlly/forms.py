from django import forms

class SignupForm(forms.Form):
    username = forms.CharField(label='Pseudo', max_length=25)
    email = forms.EmailField()
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
