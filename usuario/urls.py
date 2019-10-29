from django.urls import path
from django.conf.urls import url
from . import views

app_name = "usuario"
urlpatterns = [
    path('/cadastro_usuario', views.cadastro_usuario, name = 'cadastro_usuario'),
]