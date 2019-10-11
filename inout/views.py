from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.urls import reverse
from django.template import loader
from .models import Documento, Prazo
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime

#Metodos de controle

#View responsável por chamar o template da página de login
def login_view(request):
	return render(request, 'inout/login.html')

#View responsável por validar as credenciais recebidas no template de login
def valida_login(request):
	user = authenticate(request, username = request.POST['nome_de_usuario'], password = request.POST['senha'])

	if user is not None:
		login(request, user)
		#request.session['user_id'] = user.id
		return redirect(reverse('inout:index'))
	else:
		erro = {
			'erro': "Credenciais Inválidas",
		}

		#Renderiza a página de login novamente, com o adicional de uma mensagem de erro
		return render(request, 'inout/login.html', erro)

#View responsável por deslogar um usuário
def logout_view(request):
	#O try/except é necessário pro caso de acontecer uma tentativa de deletar uma sessão que não existe
	try:
		#Exclui a sessão
		logout(request)
		#del request.session['user_id']
	except KeyError:
		#Não faz nada
		pass

	#Redireciona para a página de login
	return redirect(reverse('inout:login_view'))

#View responsável por exibir a página inicial
@login_required
def index(request):
	#Filtra todos os documentos com prazo na data de hoje
	lista_de_documentos = prazos_do_dia()
	##Filtra todos os documentos cadastrados na data de hoje
	feitos_hoje = documentos_do_dia()
	#Filtra todos os documentos cadastrados na semana atual
	feitos_semana = documentos_da_semana()
	#Filtra todos os documentos cadastrados no mês atual
	feitos_mes = documentos_do_mes()

	#O contexto armazena as 4 informações coletadas nas linhas acima, as mesmas serão exibidas nos 4 cards presentes na página inicial
	contexto = {
		'quantidade_de_prazos_do_dia': len(lista_de_documentos),
		'feitos_hoje': len(feitos_hoje),
		'feitos_semana': len(feitos_semana),
		'feitos_mes': len(feitos_mes),
	}

	#Renderiza a página de login com o contexto gerado
	return render(request, 'inout/index.html', contexto)

	""" Tambem é possivel verificar o login para permitir o acesso as paginas usando a seguinte estrutura:
	if request.user.is_autheticated:
		faz alguma coisa
	else:
		redireciona para outra página """

@login_required
def cadastrar(request):
	contexto = {
		'titulo': "Cadastrar novo documento",
	}

	return render(request, 'inout/cadastrar.html', contexto)

#def responsavel apenas por processar dados, não carrega um template de página, apenas faz o redirecionamento para uma outra def que possua um template
@login_required
def salvarcadastro(request):
	if request.method == 'POST':
		#Cada request.POST é responsável por capturar um dado especifico do formulário, esse dado é representado pelo seu name no input do form
		documento = Documento()
		documento.usuario = request.user
		documento.data_de_entrada = datetime.date.today()
		documento.tipo_de_documento = request.POST['tipo_de_documento']
		documento.numero_do_documento = request.POST['numero_do_documento']
		documento.orgao_expedidor_do_documento = request.POST['orgao_expedidor_do_documento']
		documento.assunto_do_documento = request.POST['assunto_do_documento']
		documento.despacho_do_documento = request.POST['despacho_do_documento']
		documento.numero_do_processo = request.POST['numero_do_processo']
		documento.save()

		if (request.POST['prazo_01'] != ''):
			tipo_01 = request.POST['tipo_01']
			prazo_01 = request.POST['prazo_01']
			documento.prazo_set.create(tipo_de_prazo = tipo_01, data_do_prazo = prazo_01)
		
		try:
			tipo_02 = request.POST['tipo_02']
			prazo_02 = request.POST['prazo_02']
			documento.prazo_set.create(tipo_de_prazo = tipo_02, data_do_prazo = prazo_02)
		except:
			print("Prazo 02 não utilizado")
		
		try:
			tipo_03 = request.POST['tipo_03']
			prazo_03 = request.POST['prazo_03']
			documento.prazo_set.create(tipo_de_prazo = tipo_03, data_do_prazo = prazo_03)
		except:
			print("Prazo 03 não utilizado")

		#return HttpResponseRedirect(reverse('inout:index'))
		return redirect(reverse('inout:cadastrar'))

#Retorna um formulario preenchido com as informações de um documento já cadastrado
def editar_documento(request, documento_id):
	documento = get_object_or_404(Documento, pk = documento_id)
	contexto = {
		'titulo': "Editar " + documento.tipo_de_documento + " " + documento.numero_do_documento,
		'documento': documento,
	}

	return render(request, 'inout/editar.html', contexto)

#Retorna todos os documentos cadastrados no sistema
@login_required
def listardocumentos(request):
	lista_de_documentos = Documento.objects.order_by('data_de_entrada')
	contexto = {
		'titulo': "Todos os documentos",
		'lista_de_documentos': lista_de_documentos,
	}

	return render(request, 'inout/listardocumentos.html', contexto)

#Retorna todos os documentos cadastrados hoje
@login_required
def listar_documentos_do_dia(request):
	feitos_hoje = documentos_do_dia()
	contexto = {
		'titulo': "Documentos cadastrados hoje",
		'lista_de_documentos': feitos_hoje,
	}

	return render(request, 'inout/listardocumentos.html', contexto)

#Retorna todos os documentos cadastrados na semana atual
@login_required
def listar_documentos_da_semana(request):
	feitos_semana = documentos_da_semana()
	contexto = {
		'titulo': "Documentos cadastrados nessa semana",
		'lista_de_documentos': feitos_semana,
	}

	return render(request, 'inout/listardocumentos.html', contexto)

#Retorna todos os documentos cadastrados no mês atual
@login_required
def listar_documentos_do_mes(request):
	feitos_mes = documentos_do_mes()
	contexto = {
		'titulo': "Documentos cadastrados nesse mês",
		'lista_de_documentos': feitos_mes,
	}

	return render(request, 'inout/listardocumentos.html', contexto)

@login_required
def detalhesdocumento(request, documento_id):
	documento = get_object_or_404(Documento, pk = documento_id)
	contexto = {
		'documento': documento,
		'data_de_hoje': datetime.date.today(),
	}

	return render(request, 'inout/detalhesdocumento.html', contexto)

@login_required
def listarprazos(request):
	lista_de_documentos = Documento.objects.exclude(prazo__data_do_prazo__lt = datetime.date.today()).exclude(prazo__data_do_prazo = None)
	contexto = {
		'titulo': "Prazos para vencer",
		'lista_de_documentos': lista_de_documentos,
	}

	return render(request, 'inout/listardocumentos.html', contexto)

@login_required
def listarprazosdodia(request):
	lista_de_documentos = prazos_do_dia()

	contexto = {
		'titulo': "Prazos de hoje",
		'lista_de_documentos': lista_de_documentos,
	}

	return render(request, 'inout/listardocumentos.html', contexto)

@login_required
def alterar_status_prazo(request, documento_id, prazo_id):
	documento = get_object_or_404(Documento, pk = documento_id)
	prazo = documento.prazo_set.get(pk = prazo_id)

	if (prazo.prazo_encerrado == False):
		prazo.prazo_encerrado = True
		prazo.save()

	return redirect(reverse('inout:detalhesdocumento', args=[documento.id]))


##### DADOS DOS GRÁFICOS - criar arquivo


class chart_data_linha(APIView):
	authentication_classes = []
	permission_classes = []

	def get(self, request, format=None):

		data_de_hoje = datetime.date.today()
		documentosCadastrados = []

		for i in range(-11, 0, 1):
			documentosCadastrados.append(Documento.objects.filter(data_de_entrada__month = (data_de_hoje + relativedelta(months = i)).month).count())

		documentosCadastrados.append(len(Documento.objects.filter(data_de_entrada__month = data_de_hoje.month)))
		meses = []

		for i in range(-11, 0, 1):
			meses.append(retorna_mes((data_de_hoje + relativedelta(months = i)).month))

		meses.append(retorna_mes(datetime.date.today().month))

		dados_grafico_linha = {
			'documentosCadastrados': documentosCadastrados,
			'meses': meses,
		}

		return Response(dados_grafico_linha)

class chart_data_pie(APIView):
	authentication_classes = []
	permission_classes = []

	def get(self, request, format=None):

		quantidadeTipoDocumento = [
			len(Documento.objects.filter(tipo_de_documento = "Ofício")),
			len(Documento.objects.filter(tipo_de_documento = "Ofício Circular")),
			len(Documento.objects.filter(tipo_de_documento = "Memorando")),
			len(Documento.objects.filter(tipo_de_documento = "Memorando Circular")),
			len(Documento.objects.exclude(tipo_de_documento = "Ofício").exclude(tipo_de_documento = "Ofício Circular").exclude(tipo_de_documento = "Memorando").exclude(tipo_de_documento = "Memorando Circular")),
			#len(Documento.objects.filter(tipo_de_documento = "Requerimento")),
			#len(Documento.objects.filter(tipo_de_documento = "Mandado de Intimação")),
			#len(Documento.objects.filter(tipo_de_documento = "Notificação")),
			#len(Documento.objects.filter(tipo_de_documento = "Documento")),
		]

		tiposDeDocumento = [
			"Ofício",
			"Ofício Circular",
			"Memorando",
			"Memorando Circular",
			"Outros",
			#"Requerimento",
			#"Mandado de Intimação",
			#"Notificação",
			#"Documento",
		]

		dados_grafico_pie = {
			'quantidadeTipoDocumento': quantidadeTipoDocumento,
			'tiposDeDocumento': tiposDeDocumento,
		}

		return Response(dados_grafico_pie)


##### FUNÇÕES - criar arquivo


def prazos_do_dia():
	lista_de_documentos = Documento.objects.filter(prazo__data_do_prazo = datetime.date.today())

	return lista_de_documentos

#Retorna todos os documentos cadastrados no dia de hoje
def documentos_do_dia():
	feitos_hoje = Documento.objects.filter(data_de_entrada__day = datetime.date.today().day)

	return feitos_hoje

#Retorna todos os documentos cadastrados na semana atual
def documentos_da_semana():
	feitos_semana = Documento.objects.filter(data_de_entrada__week = datetime.date.today().isocalendar()[1])

	return feitos_semana

#Retorna todos os documentos cadastrados no mês atual
def documentos_do_mes():
	feitos_mes = Documento.objects.filter(data_de_entrada__month = datetime.date.today().month)

	return feitos_mes

def retorna_mes(mes_numero):
	lista = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

	return lista[mes_numero - 1]