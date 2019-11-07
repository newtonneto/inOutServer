from django.urls import path
from django.conf.urls import url, re_path
from . import views

app_name = "usuario"
urlpatterns = [
    re_path(r'^cadastro_usuario/', views.cadastro_usuario, name = 'cadastro_usuario'),
    re_path(r'^salva_usuario/', views.salva_usuario, name = 'salva_usuario'),
]