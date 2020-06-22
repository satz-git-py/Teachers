from django.urls import path
from directory import views

app_name = 'directory'

urlpatterns = [
    path('', views.profile, name='director'),
]
