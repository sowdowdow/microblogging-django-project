from django.urls import path, include
from Microlly import views

app_name = "Microlly"


urlpatterns = [
    path("", views.index, name="index"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('account/', views.account, name="account"),
    path('accounts/signup/', views.signup, name='signup'),
]
