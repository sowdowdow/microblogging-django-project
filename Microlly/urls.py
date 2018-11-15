from django.urls import path
from Microlly import views
app_name = 'Microlly'


urlpatterns = [
    path('', views.index, name='index'),
]