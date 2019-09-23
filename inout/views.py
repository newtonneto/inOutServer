from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.urls import reverse
from django.template import loader
#from django.utils import timezone
from .models import Documento, Usuario, Prazo
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime
import calendar
import json

#Metodos de controle

#View responsável por chamar o template da página de login
def login(request):
	return render(request, 'inout/login.html')

#View responsável por validar as credenciais recebidas no template de login
def valida_login(request):
	#O try/except é necessário pro caso do nome de usuário informado ser inválido, sem ele o código encontraria um erro ao tentar capturar informações de objetos que não existem (usuários inválidos)
	try:
		#Faz uma busca no banco pelo usuário informado, caso seja encontrado, o objeto será armazenado na variavel usuário
		usuario = Usuario.objects.get(nome_de_usuario = request.POST['nome_de_usuario'])
		#Verifica se a senha armazenada no objeto é a mesma informada no formulario de login
		if (usuario.senha == request.POST['senha']):
			#Armazena nos cookies o id do objeto usuário
			request.session['usuario_id'] = usuario.id

			#Redireciona para o index
			return redirect(reverse('inout:index'))
	except Usuario.DoesNotExist:
		erro = {
			'erro': "Credenciais Inválidas",
		}

		#Renderiza a página de login novamente, com o adicional de uma mensagem de erro
		return render(request, 'inout/login.html', erro)

#View responsável por deslogar um usuário
def logout(request):
	#O try/except é necessário pro caso de acontecer uma tentativa de deletar uma sessão que não existe
	try:
		#Exclui a sessão
		del request.session['usuario_id']
	except KeyError:
		#Não faz nada
		pass

	#Redireciona para a página de login
	return redirect(reverse('inout:login'))

#View responsável por exibir a página inicial
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

def cadastrar(request):
	contexto = {
		'titulo': "Cadastrar novo documento",
	}

	return render(request, 'inout/cadastrar.html', contexto)

#def responsavel apenas por processar dados, não carrega um template de página, apenas faz o redirecionamento para uma outra def que possua um template
def salvarcadastro(request):
	if request.method == 'POST':
		#Cada request.POST é responsável por capturar um dado especifico do formulário, esse dado é representado pelo seu name no input do form
		data_de_entrada = datetime.date.today()
		tipo_de_documento = request.POST['tipo_de_documento']
		numero_do_documento = request.POST['numero_do_documento']
		orgao_expedidor_do_documento = request.POST['orgao_expedidor_do_documento']
		assunto_do_documento = request.POST['assunto_do_documento']
		despacho_do_documento = request.POST['despacho_do_documento']
		numero_do_processo = request.POST['numero_do_processo']
		documento = Documento(data_de_entrada = data_de_entrada, tipo_de_documento = tipo_de_documento, numero_do_documento = numero_do_documento, orgao_expedidor_do_documento = orgao_expedidor_do_documento, assunto_do_documento = assunto_do_documento, despacho_do_documento = despacho_do_documento, numero_do_processo = numero_do_processo)
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

#Retorna todos os documentos cadastrados no sistema
def listardocumentos(request):
	lista_de_documentos = Documento.objects.order_by('data_de_entrada')
	contexto = {
		'titulo': "Todos os documentos",
		'lista_de_documentos': lista_de_documentos,
	}

	return render(request, 'inout/listardocumentos.html', contexto)

#Retorna todos os documentos cadastrados hoje
def listar_documentos_do_dia(request):
	feitos_hoje = documentos_do_dia()
	contexto = {
		'titulo': "Documentos cadastrados hoje",
		'lista_de_documentos': feitos_hoje,
	}

	return render(request, 'inout/listardocumentos.html', contexto)

#Retorna todos os documentos cadastrados na semana atual
def listar_documentos_da_semana(request):
	feitos_semana = documentos_da_semana()
	contexto = {
		'titulo': "Documentos cadastrados nessa semana",
		'lista_de_documentos': feitos_semana,
	}

	return render(request, 'inout/listardocumentos.html', contexto)

#Retorna todos os documentos cadastrados no mês atual
def listar_documentos_do_mes(request):
	feitos_mes = documentos_do_mes()
	contexto = {
		'titulo': "Documentos cadastrados nesse mês",
		'lista_de_documentos': feitos_mes,
	}

	return render(request, 'inout/listardocumentos.html', contexto)

def detalhesdocumento(request, documento_id):
	try:
		documento = Documento.objects.get(pk = documento_id)
		contexto = {
			'documento': documento,
			'data_de_hoje': datetime.date.today(),
		}
	except Documento.DoesNotExist:
		raise Http404("Documento não ecziste")

	return render(request, 'inout/detalhesdocumento.html', contexto)

def listarprazos(request):
	lista_de_documentos = Documento.objects.exclude(prazo__data_do_prazo__lt = datetime.date.today()).exclude(prazo__data_do_prazo = None)
	contexto = {
		'titulo': "Prazos para vencer",
		'lista_de_documentos': lista_de_documentos,
	}

	return render(request, 'inout/listardocumentos.html', contexto)

def listarprazosdodia(request):
	#lista_de_documentos = Documento.objects.filter(prazo__data_do_prazo = datetime.date.today()) #Depois de validar, substituir por função prazos_do_dia
	lista_de_documentos = prazos_do_dia()

	contexto = {
		'titulo': "Prazos de hoje",
		'lista_de_documentos': lista_de_documentos,
	}

	return render(request, 'inout/listardocumentos.html', contexto)

def alterar_status_prazo(request, documento_id, prazo_id):
	documento = Documento.objects.get(pk = documento_id)
	prazo = documento.prazo_set.get(pk = prazo_id)

	if (prazo.prazo_encerrado == False):
		prazo.prazo_encerrado = True
		prazo.save()

	return redirect(reverse('inout:detalhesdocumento', args=[documento.id]))

##### DADOS DOS GRÁFICOS - criar arquivo


def dados_grafico_linha(request):
	dados_grafico_linha = {
		'mes1' : len(Documento.objects.filter(data_de_entrada__month = datetime.date.today().month)),
		'mes2' : len(Documento.objects.filter(data_de_entrada__month = datetime.date.today().month)),
		'mes3' : len(Documento.objects.filter(data_de_entrada__month = datetime.date.today().month)),
		'mes4' : len(Documento.objects.filter(data_de_entrada__month = datetime.date.today().month)),
		'mes5' : len(Documento.objects.filter(data_de_entrada__month = datetime.date.today().month)),
		'mes6' : len(Documento.objects.filter(data_de_entrada__month = datetime.date.today().month)),
		'mes7' : len(Documento.objects.filter(data_de_entrada__month = datetime.date.today().month)),
		'mes8' : len(Documento.objects.filter(data_de_entrada__month = datetime.date.today().month)),
		'mes9' : len(Documento.objects.filter(data_de_entrada__month = datetime.date.today().month)),
		'mes10' : len(Documento.objects.filter(data_de_entrada__month = datetime.date.today().month)),
		'mes11' : len(Documento.objects.filter(data_de_entrada__month = datetime.date.today().month)),
		'mes12' : len(Documento.objects.filter(data_de_entrada__month = datetime.date.today().month))
	}

	return JsonResponse(dados_grafico_linha)

class chart_data_linha(APIView):
	authentication_classes = []
	permission_classes = []

	def get(self, request, format=None):

		documentosCadastrados = [
			len(Documento.objects.filter(data_de_entrada__month = (datetime.date.today() + relativedelta(months = -11)).month)),
			len(Documento.objects.filter(data_de_entrada__month = (datetime.date.today() + relativedelta(months = -10)).month)),
			len(Documento.objects.filter(data_de_entrada__month = (datetime.date.today() + relativedelta(months = -9)).month)),
			len(Documento.objects.filter(data_de_entrada__month = (datetime.date.today() + relativedelta(months = -8)).month)),
			len(Documento.objects.filter(data_de_entrada__month = (datetime.date.today() + relativedelta(months = -7)).month)),
			len(Documento.objects.filter(data_de_entrada__month = (datetime.date.today() + relativedelta(months = -6)).month)),
			len(Documento.objects.filter(data_de_entrada__month = (datetime.date.today() + relativedelta(months = -5)).month)),
			len(Documento.objects.filter(data_de_entrada__month = (datetime.date.today() + relativedelta(months = -4)).month)),
			len(Documento.objects.filter(data_de_entrada__month = (datetime.date.today() + relativedelta(months = -3)).month)),
			len(Documento.objects.filter(data_de_entrada__month = (datetime.date.today() + relativedelta(months = -2)).month)),
			len(Documento.objects.filter(data_de_entrada__month = (datetime.date.today() + relativedelta(months = -1)).month)),
			len(Documento.objects.filter(data_de_entrada__month = datetime.date.today().month))
		]

		meses = [
			#retorna_mes((datetime.date.today() + relativedelta(months = -11)).month) + "/" + str((datetime.date.today() + relativedelta(months = -11)).year),
			retorna_mes((datetime.date.today() + relativedelta(months = -11)).month),
			retorna_mes((datetime.date.today() + relativedelta(months = -10)).month),
			retorna_mes((datetime.date.today() + relativedelta(months = -9)).month),
			retorna_mes((datetime.date.today() + relativedelta(months = -8)).month),
			retorna_mes((datetime.date.today() + relativedelta(months = -7)).month),
			retorna_mes((datetime.date.today() + relativedelta(months = -6)).month),
			retorna_mes((datetime.date.today() + relativedelta(months = -5)).month),
			retorna_mes((datetime.date.today() + relativedelta(months = -4)).month),
			retorna_mes((datetime.date.today() + relativedelta(months = -3)).month),
			retorna_mes((datetime.date.today() + relativedelta(months = -2)).month),
			retorna_mes((datetime.date.today() + relativedelta(months = -1)).month),
			retorna_mes(datetime.date.today().month)
		]

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
			len(Documento.objects.exclude(tipo_de_documento = "Ofício").exclude(tipo_de_documento = "Ofício Circular").exclude(tipo_de_documento = "Memorando").exclude(tipo_de_documento = "Memorando Circular"))
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
	#feitos_mes = Documento.objects.filter(data_de_entrada__month = (datetime.date.today()-timedelta(weeks=4)).month)
	#feitos_mes = Documento.objects.filter(data_de_entrada__month = (datetime.date.today() + relativedelta(months = -1)).month)

	return feitos_mes

def retorna_mes(mes_numero):
	if (mes_numero == 1):

		return "Janeiro"

	elif (mes_numero == 2):

		return "Fevereiro"

	elif (mes_numero == 3):

		return "Março"

	elif (mes_numero == 4):

		return "Abril"

	elif (mes_numero == 5):

		return "Maio"

	elif (mes_numero == 6):

		return "Junho"

	elif (mes_numero == 7):

		return "Julho"

	elif (mes_numero == 8):

		return "Agosto"

	elif (mes_numero == 9):

		return "Setembro"

	elif (mes_numero == 10):

		return "Outubro"

	elif (mes_numero == 11):

		return "Novembro"
	
	else:

		return "Dezembro"