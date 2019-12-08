from django.urls import path
from django.conf.urls import url, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views
#from inout.views import lista_protocolos

app_name = "inout"
urlpatterns = [
	#path('', views.index, name = 'index'),
	#path('', views.login_view, name = 'login_view'),
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
	path('<int:documento_id>/salvar_edicao_documento', views.salvar_edicao_documento, name = 'salvar_edicao_documento'),
	re_path(r'^protocolar_documento', views.protocolar_documento, name = "protocolar_documento"),
	re_path(r'^salvar_protocolo_documento', views.salvar_protocolo_documento, name = "salvar_protocolo_documento"),
	path('<int:protocolo_documento_id>/documento_entregue', views.documento_entregue, name = "documento_entregue"),
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
	re_path(r'^novo_orgao', views.novo_orgao, name = 'novo_orgao'),
	re_path(r'^salvar_orgao', views.salvar_orgao, name = 'salvar_orgao'),
	re_path(r'^lista_orgaos', views.lista_orgaos , name = "lista_orgaos"),
	re_path(r'^novo_setor', views.novo_setor , name = "novo_setor"),
	re_path(r'^salvar_setor', views.salvar_setor , name = "salvar_setor"),
	re_path(r'^lista_setores', views.lista_setores , name = "lista_setores"),
	re_path(r'^novo_protocolo', views.novo_protocolo , name = "novo_protocolo"),
	re_path(r'^salvar_protocolo', views.salvar_protocolo , name = "salvar_protocolo"),
	re_path(r'^lista_protocolos_externos', views.lista_protocolos_externos , name = "lista_protocolos_externos"),
	re_path(r'^lista_protocolos_internos', views.lista_protocolos_internos , name = "lista_protocolos_internos"),
	re_path(r'^lista_protocolos_usf', views.lista_protocolos_usf , name = "lista_protocolos_usf"),
	#re_path(r'^lista_protocolos', lista_protocolos.as_view(), name = "lista_protocolos"),
	re_path(r'^busca_numero_documento', views.busca_numero_documento, name = 'busca_numero_documento'),
	url(r'^api/chart/data/$', views.chart_data_linha.as_view()),
	url(r'^api/chart/pie/$', views.chart_data_pie.as_view()),
	#Falta implementar
	re_path(r'^busca_avancada', views.busca_avancada , name = "busca_avancada"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)