from django.urls import path
from django.contrib.auth.views import LoginView
from Microlly import views

app_name = "Microlly"


urlpatterns = [
    path("", views.index, name="index"),
    path("login/", LoginView.as_view(), name="login"),
]
