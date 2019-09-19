from django.urls import path
from . import views

app_name = "inout"
urlpatterns = [
	path('', views.login, name = 'login'),
	path('login', views.login, name = 'login'),
	path('login.html', views.login, name = 'login'),
	path('valida_login', views.valida_login, name = 'valida_login'),
	path('index', views.index, name = 'index'),
	path('index.html', views.index, name = 'index'),
	path('cadastrar', views.cadastrar, name = 'cadastrar'),
	#path('cadastrar.html', views.cadastrar, name = 'cadastrar'),
	path('salvarcadastro', views.salvarcadastro, name = 'salvarcadastro'),
	path('listardocumentos', views.listardocumentos, name = 'listardocumentos'),
	#path('listardocumentos.html', views.listardocumentos, name = 'listardocumentos'),
	path('<int:documento_id>/detalhesdocumento', views.detalhesdocumento, name = 'detalhesdocumento'),
	#path('<int:documento_id>/detalhesdocumento.html', views.detalhesdocumento, name = 'detalhesdocumento'),
	path('listarprazos', views.listarprazos, name = 'listarprazos'),
	#path('listarprazos.html', views.listarprazos, name = 'listarprazos'),
	path('listarprazosdodia', views.listarprazosdodia, name = 'listarprazosdodia'),
	#path('listarprazosdodia.html', views.listarprazosdodia, name = 'listarprazosdodia'),
	path('listar_documentos_do_dia', views.listar_documentos_do_dia, name = 'listar_documentos_do_dia'),
	path('listar_documentos_da_semana', views.listar_documentos_da_semana, name = 'listar_documentos_da_semana'),
	path('listar_documentos_do_mes', views.listar_documentos_do_mes, name = 'listar_documentos_do_mes'),
]