from django.urls import path
from django.conf.urls import url
from . import views

app_name = "inout"
urlpatterns = [
	path('', views.login_view, name = 'login_view'),
	path('login', views.login_view, name = 'login_view'),
	path('login.html', views.login_view, name = 'login_view'),
	path('valida_login', views.valida_login, name = 'valida_login'),
	path('logout', views.logout_view, name = 'logout_view'),
	path('index', views.index, name = 'index'),
	path('index.html', views.index, name = 'index'),
	path('cadastrar', views.cadastrar, name = 'cadastrar'),
	path('cadastrar.html', views.cadastrar, name = 'cadastrar'),
	path('salvarcadastro', views.salvarcadastro, name = 'salvarcadastro'),
	path('<int:documento_id>/editar_documento', views.editar_documento, name = 'editar_documento'),
	path('listardocumentos', views.listardocumentos, name = 'listardocumentos'),
	path('listardocumentos.html', views.listardocumentos, name = 'listardocumentos'),
	path('<int:documento_id>/detalhesdocumento', views.detalhesdocumento, name = 'detalhesdocumento'),
	path('<int:documento_id>/detalhesdocumento.html', views.detalhesdocumento, name = 'detalhesdocumento'),
	path('<int:documento_id>/<int:prazo_id>/alterar_status_prazo', views.alterar_status_prazo, name = 'alterar_status_prazo'),
	path('listarprazos', views.listarprazos, name = 'listarprazos'),
	path('listarprazos.html', views.listarprazos, name = 'listarprazos'),
	path('listarprazosdodia', views.listarprazosdodia, name = 'listarprazosdodia'),
	path('listarprazosdodia.html', views.listarprazosdodia, name = 'listarprazosdodia'),
	path('listar_documentos_do_dia', views.listar_documentos_do_dia, name = 'listar_documentos_do_dia'),
	path('listar_documentos_da_semana', views.listar_documentos_da_semana, name = 'listar_documentos_da_semana'),
	path('listar_documentos_do_mes', views.listar_documentos_do_mes, name = 'listar_documentos_do_mes'),
	url(r'^api/chart/data/$', views.chart_data_linha.as_view()),
	url(r'^api/chart/pie/$', views.chart_data_pie.as_view()),
]