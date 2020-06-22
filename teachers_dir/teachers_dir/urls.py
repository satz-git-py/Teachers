from django.contrib import admin
from django.urls import path, include
from directory import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.directory, name='directory'),
    path('<int:teach_id>', include('directory.urls', namespace='directory')),
]
