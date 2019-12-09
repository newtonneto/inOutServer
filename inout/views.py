from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404
from django.urls import reverse
from django.template import loader
from .models import Documento, Prazo, Processo, Orgao, Setor, Livro, Pagina, Protocolo, Lotacao
from django.db import connections
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime

cursor_mysql = connections['default'].cursor()
cursor_postgresql = connections['postgresql'].cursor()

#Metodos de controle

#View responsável por chamar o template da página de login
def login_view(request):

	return render(request, 'registration/login.html')

#View responsável por validar as credenciais recebidas no template de login
def valida_login(request):
	user = authenticate(request, username = request.POST['nome_de_usuario'], password = request.POST['senha'])

	if user is not None:
		login(request, user)
		#Recupera o parametro next
		next = request.POST.get('next', False)

		if next:
			return redirect(reverse("{}{}".format('inout:', next.replace('/', '').replace('.html', ''))))
		else:
			return redirect(reverse('inout:index'))
	else:
		erro = {
			'erro': "Credenciais Inválidas",
		}

		#Renderiza a página de login novamente, com o adicional de uma mensagem de erro
		return render(request, 'registration/login.html', erro)

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
	return render(request, 'index.html', contexto)

	""" Tambem é possivel verificar o login para permitir o acesso as paginas usando a seguinte estrutura:
	if request.user.is_autheticated:
		faz alguma coisa
	else:
		redireciona para outra página """

@login_required
def cadastrar(request):
	prazo = Prazo()

	contexto = {
		'titulo': "Cadastrar novo documento",
		'lista_de_tipos_de_prazo': prazo.tipo_choices
	}

	return render(request, 'inout/cadastrar.html', contexto)

#def responsavel apenas por processar dados, não carrega um template de página, apenas faz o redirecionamento para uma outra def que possua um template
@login_required
def salvarcadastro(request):
	if request.method == 'POST':
		#Cada request.POST é responsável por capturar um dado especifico do formulário, esse dado é representado pelo seu name no input do form
		""" documento = Documento()
		documento.fk_user = request.user
		documento.data_de_recebimento = datetime.date.today()
		documento.tipo = int(request.POST['tipo_de_documento'])
		documento.numero = request.POST['numero_do_documento']
		documento.emissor = request.POST['orgao_expedidor_do_documento']
		documento.assunto = request.POST['assunto_do_documento']
		documento.despacho = request.POST['despacho_do_documento'] """

		cursor_mysql.execute('INSERT INTO documento '
								+ '(fk_user, data_de_recebimento, tipo, numero, emissor, assunto, despacho, entrega_pessoal) '
							+ 'VALUES '
								+ '(%s, %s, %s, %s, %s, %s, %s, %s)', [
																		request.user.id,
																		datetime.date.today(),
																		int(request.POST['tipo_de_documento']),
																		request.POST['numero_do_documento'],
																		request.POST['orgao_expedidor_do_documento'],
																		request.POST['assunto_do_documento'],
																		request.POST['despacho_do_documento'],
																		request.POST.get('entrega_pessoal', False),
																		])
		cursor_mysql.execute('SELECT MAX(id) FROM documento')
		documento_id = cursor_mysql.fetchone()[0]

		documento_pdf = Documento.objects.using('default').get(pk = documento_id)
		documento_pdf.pdf = request.FILES["pdf"]
		documento_pdf.save()

		cursor_postgresql.execute('INSERT INTO documento '
									+ '(fk_user, data_de_recebimento, tipo, numero, emissor, assunto, despacho, entrega_pessoal) '
								+ 'VALUES '
									+ '(%s, %s, %s, %s, %s, %s, %s, %s)', [
																			request.user.id,
																			datetime.date.today(),
																			int(request.POST['tipo_de_documento']),
																			request.POST['numero_do_documento'],
																			request.POST['orgao_expedidor_do_documento'],
																			request.POST['assunto_do_documento'],
																			request.POST['despacho_do_documento'],
																			request.POST.get('entrega_pessoal', False),
																			])
		cursor_postgresql.execute('SELECT MAX(id) FROM documento')
		documento_id = cursor_postgresql.fetchone()[0]

		documento_pdf = Documento.objects.using('postgresql').get(pk = documento_id)
		documento_pdf.pdf = request.FILES["pdf"]
		documento_pdf.save()

		""" try:
			#Tenta recuperar o objeto do processo com o número informado no formulário
			processo = Processo.objects.get(numero = request.POST['numero_do_processo'])
			#Caso seja, o documento é associado ao processo
			documento.processo = processo
		except Processo.DoesNotExist:
			#Caso não seja, é criado um novo processo, e então o documento é associado a ele
			novo_processo = Processo()
			novo_processo.numero = request.POST['numero_do_processo']
			novo_processo.save()
			documento.processo = novo_processo """

		processo = request.POST.get('numero_do_processo', False)
		if processo:
			objeto_processo = Processo.objects.using('default').raw('SELECT * FROM processo WHERE numero = %s', [processo])
			if objeto_processo:
				#with connection.cursor() as cursor:
				cursor_mysql.execute('UPDATE documento SET fk_processo = %s WHERE id = %s', [objeto_processo[0].id, documento_id])
			else:
				#with connection.cursor() as cursor:
				cursor_mysql.execute('INSERT INTO processo (numero) VALUES (%s)', [processo])
				cursor_mysql.execute('SELECT MAX(id) FROM processo')
				objeto_processo_id = cursor_mysql.fetchone()[0]
				cursor_mysql.execute('UPDATE documento SET fk_processo = %s WHERE id = %s', [objeto_processo_id, documento_id])

			objeto_processo = Processo.objects.using('postgresql').raw('SELECT * FROM processo WHERE numero = %s', [processo])
			if objeto_processo:
				#with connection.cursor() as cursor:
				cursor_postgresql.execute('UPDATE documento SET fk_processo = %s WHERE id = %s', [objeto_processo[0].id, documento_id])
			else:
				#with connection.cursor() as cursor:
				cursor_postgresql.execute('INSERT INTO processo (numero) VALUES (%s)', [processo])
				cursor_postgresql.execute('SELECT MAX(id) FROM processo')
				objeto_processo_id = cursor_postgresql.fetchone()[0]
				cursor_postgresql.execute('UPDATE documento SET fk_processo = %s WHERE id = %s', [objeto_processo_id, documento_id])

		#Salva o novo documento
		#documento.save()

		""" if (request.POST['prazo_01'] != ''):
			tipo_01 = request.POST['tipo_01']
			prazo_01 = request.POST['prazo_01']
			documento.prazo_set.create(tipo = tipo_01, vencimento = prazo_01)
		
		try:
			tipo_02 = request.POST['tipo_02']
			prazo_02 = request.POST['prazo_02']
			documento.prazo_set.create(tipo = tipo_02, vencimento = prazo_02)
		except:
			print("Prazo 02 não utilizado")
		
		try:
			tipo_03 = request.POST['tipo_03']
			prazo_03 = request.POST['prazo_03']
			documento.prazo_set.create(tipo = tipo_03, vencimento = prazo_03)
		except:
			print("Prazo 03 não utilizado") """
		indice = 1
		
		while True:
			tipo = "{}{}".format("tipo_", indice)
			data = "{}{}".format("prazo_", indice)
			prazo_tipo = request.POST.get(tipo, False)
			prazo_data = request.POST.get(data, False)

			if prazo_tipo and prazo_data:
				cursor_mysql.execute('INSERT INTO prazo '
										+ '(fk_documento, tipo, vencimento, encerrado, dilacao) '
									+ 'VALUES '
										+ '(%s, %s, %s, false, false)', [
																			documento_id,
																			prazo_tipo,
																			prazo_data,
																			])

				cursor_postgresql.execute('INSERT INTO prazo '
											+ '(fk_documento, tipo, vencimento, encerrado, dilacao) '
										+ 'VALUES '
											+ '(%s, %s, %s, false, false)', [
																				documento_id,
																				prazo_tipo,
																				prazo_data,
																				])
			else:
				break
			indice += 1

		#return HttpResponseRedirect(reverse('inout:index'))
		return redirect(reverse('inout:cadastrar'))

#Retorna um formulario preenchido com as informações de um documento já cadastrado
def editar_documento(request, documento_id):
	try:
		documento = Documento.objects.raw('SELECT * FROM documento WHERE id = %s', [documento_id])[0]
	except Documento.DoesNotExist:
		return redirect(reverse('inout:error_404_view'))
	
	contexto = {
		'titulo': "Editar " + documento.tipo_do_documento() + " " + documento.numero,
		'documento': documento,
	}

	return render(request, 'inout/editar.html', contexto)

def salvar_edicao_documento(request, documento_id):
	if request.method == "POST":
		cursor_mysql.execute('UPDATE documento SET '
								+ 'tipo = %s, '
								+ 'numero = %s, '
								+ 'emissor = %s, '
								+ 'assunto = %s, '
								+ 'despacho = %s '
							+ 'WHERE '
								+ 'id = %s', [
												int(request.POST['tipo_de_documento']),
												request.POST['numero_do_documento'],
												request.POST['orgao_expedidor_do_documento'],
												request.POST['assunto_do_documento'],
												request.POST['despacho_do_documento'],
												documento_id,
												])

		cursor_postgresql.execute('UPDATE documento SET '
									+ 'tipo = %s, '
									+ 'numero = %s, '
									+ 'emissor = %s, '
									+ 'assunto = %s, '
									+ 'despacho = %s '
								+ 'WHERE '
									+ 'id = %s', [
													int(request.POST['tipo_de_documento']),
													request.POST['numero_do_documento'],
													request.POST['orgao_expedidor_do_documento'],
													request.POST['assunto_do_documento'],
													request.POST['despacho_do_documento'],
													documento_id,
													])

		return redirect(reverse('inout:listardocumentos'))

#Retorna todos os documentos cadastrados no sistema
@login_required
def listardocumentos(request):
	#lista_de_documentos = Documento.objects.order_by('data_de_recebimento')
	lotacao_user = Lotacao.objects.raw('SELECT * FROM lotacao WHERE fk_user = %s', [request.user.id])
	lista_de_documentos = Documento.objects.raw('SELECT * FROM documento INNER JOIN lotacao ON lotacao.fk_user = documento.fk_user WHERE fk_setor = %s', [lotacao_user[0].fk_setor.id])

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
	""" documento = get_object_or_404(Documento, pk = documento_id) """
	try:
		documento = Documento.objects.raw('SELECT * FROM documento WHERE id = %s', [documento_id])[0]
	except Documento.DoesNotExist:
		return redirect(reverse('inout:error_404_view'))

	protocolo_documento = Protocolo.objects.raw('SELECT * FROM protocolo WHERE fk_documento = %s', [documento_id])

	if protocolo_documento:
		contexto = {
			'documento': documento,
			'protocolo_documento': protocolo_documento[0],
			'data_de_hoje': datetime.date.today(),
		}
	
	else:
		contexto = {
			'documento': documento,
			'data_de_hoje': datetime.date.today(),
		}

	return render(request, 'inout/detalhesdocumento.html', contexto)

@login_required
def documento_entregue(request, protocolo_documento_id):
	cursor_mysql.execute('UPDATE protocolo SET '
							+ 'entregue = true, '
							+ 'data_da_entrega = %s '
						+ 'WHERE '
							+ 'id = %s', [
											datetime.date.today(),
											protocolo_documento_id
											])

	cursor_postgresql.execute('UPDATE protocolo SET '
								+ 'entregue = true, '
								+ 'data_da_entrega = %s '
							+ 'WHERE '
								+ 'id = %s', [
												datetime.date.today(),
												protocolo_documento_id
												])
	
	return redirect(reverse('inout:listardocumentos'))

@login_required
def listarprazos(request):
	lista_de_documentos = Documento.objects.using('default').raw('SELECT * FROM documento INNER JOIN prazo ON prazo.fk_documento = documento.id WHERE prazo.vencimento >= %s', [datetime.date.today()])
	#lista_de_documentos = Documento.objects.exclude(prazo__vencimento__lt = datetime.date.today()).exclude(prazo__vencimento = None)

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
	""" documento = get_object_or_404(Documento, pk = documento_id)
	prazo = documento.prazo_set.get(pk = prazo_id)

	if (prazo.encerrado == False):
		prazo.encerrado = True
		prazo.save() """
	#with connection.cursor() as cursor:
	cursor_mysql.execute('UPDATE prazo SET '
							+ 'encerrado = true '
						+ 'WHERE '
							+ 'id = %s', [
											prazo_id
											])

	cursor_postgresql.execute('UPDATE prazo SET '
								+ 'encerrado = true '
							+ 'WHERE '
								+ 'id = %s', [
												prazo_id
												])

	return redirect(reverse('inout:detalhesdocumento', args=[documento_id]))

@login_required
def novo_orgao(request):
	contexto = {
		'titulo': "Cadastrar novo orgão",
	}

	return render(request, 'inout/novo_orgao.html', contexto)

@login_required
def salvar_orgao(request):
	nome = request.POST.get("nome", False)
	sigla = request.POST.get("sigla", False)
	esfera = request.POST.get("esfera", False)
	estado = request.POST.get("estado", False)
	municipio = request.POST.get("municipio", False)

	if nome and sigla and esfera and estado and municipio:
		""" orgao = Orgao()
		orgao.nome = nome
		orgao.sigla = sigla
		orgao.esfera = esfera
		orgao.estado = estado
		orgao.municipio = municipio
		orgao.save() """

		cursor_mysql.execute('INSERT INTO orgao '
								+ '(nome, sigla, esfera, estado, municipio, ativo) '
							+ 'VALUES '
								+ '(%s, %s, %s, %s, %s, true)', [
																	nome,
																	sigla,
																	esfera,
																	estado,
																	municipio,
																])

		cursor_postgresql.execute('INSERT INTO orgao '
									+ '(nome, sigla, esfera, estado, municipio, ativo) '
								+ 'VALUES '
									+ '(%s, %s, %s, %s, %s, true)', [
																		nome,
																		sigla,
																		esfera,
																		estado,
																		municipio,
																	])

		messages.add_message(request, messages.SUCCESS, "Orgão cadastrado com sucesso")
		return redirect(reverse('inout:novo_orgao'))

	else:
		messages.add_message(request, messages.ERROR, "Preencha todos os campos")
		return redirect(reverse('inout:novo_orgao'))

@login_required
def lista_orgaos(request):
	lista_de_orgaos = Orgao.objects.using('default').raw('SELECT * FROM orgao')

	context = {
		'titulo': "Lista de órgãos",
		'lista_de_orgaos': lista_de_orgaos,
	}

	return render(request, 'inout/lista_orgaos.html', context)

@login_required
def novo_setor(request):
	lista_de_orgaos = Orgao.objects.using('default').raw('SELECT * FROM orgao')

	context = {
		'titulo': "Cadastrar setor",
		'lista_de_orgaos': lista_de_orgaos,
	}

	return render(request, 'inout/novo_setor.html', context)

@login_required
def salvar_setor(request):
	nome = request.POST.get("nome", False)
	sigla = request.POST.get("sigla", False)
	orgao = request.POST.get("orgao", False)

	if nome and sigla and orgao:
		cursor_mysql.execute('INSERT INTO setor '
								+ '(fk_orgao, nome, sigla, ativo) '
							+ 'VALUES '
								+ '(%s, %s, %s, true)', [
															orgao,
															nome,
															sigla,
														])

		cursor_postgresql.execute('INSERT INTO setor '
									+ '(fk_orgao, nome, sigla, ativo) '
								+ 'VALUES '
									+ '(%s, %s, %s, true)', [
																orgao,
																nome,
																sigla,
															])

		messages.add_message(request, messages.SUCCESS, "Setor cadastrado com sucesso")
		return redirect(reverse('inout:novo_setor'))

	else:
		messages.add_message(request, messages.ERROR, "Preencha todos os campos")
		return redirect(reverse('inout:novo_setor'))

@login_required
def lista_setores(request):
	lista_de_setores = Setor.objects.using('default').raw('SELECT * FROM setor INNER JOIN orgao ON setor.fk_orgao = orgao.id ORDER BY orgao.sigla')

	context = {
		'titulo': "Lista de setores por órgão",
		'lista_de_setores': lista_de_setores,
	}

	return render(request, 'inout/lista_setores.html', context)

@login_required
def novo_protocolo(request):
	lotacao_user = Lotacao.objects.using('default').raw('SELECT * FROM lotacao WHERE fk_user = %s', [request.user.id])
	meu_setor = Setor.objects.using('default').raw('SELECT * FROM setor WHERE id = %s', [lotacao_user[0].fk_setor.id])
	
	context = {
		'titulo': "Cadastrar protocolo",
		'ano': datetime.date.today().year,
		'meu_setor': meu_setor[0],
	}

	return render(request, 'inout/novo_protocolo.html', context)

@login_required
def salvar_protocolo(request):
	lotacao_user = Lotacao.objects.using('default').raw('SELECT * FROM lotacao WHERE fk_user = %s', [request.user.id])
	ano = datetime.date.today().year
	#volume = request.POST.get("volume", False)
	setor = Setor.objects.using('default').raw('SELECT * FROM setor WHERE id = %s', [lotacao_user[0].fk_setor.id])
	tipo = request.POST.get("tipo", False)
	ultimo_volume = Livro.objects.using('default').raw('SELECT * FROM livro WHERE id = (SELECT MAX(id) FROM livro WHERE fk_setor = %s AND tipo = %s)', [lotacao_user[0].fk_setor.id, tipo])
	
	try:
		volume = (ultimo_volume[0].volume) + 1
	except:
		volume = 1

	if ano and volume and setor[0].id and tipo:
		cursor_mysql.execute('INSERT INTO livro '
								+ '(fk_setor, tipo, ano, volume, encerrado) '
							+ 'VALUES '
								+ '(%s, %s, %s, %s, false)', [
																setor[0].id,
																tipo,
																ano,
																volume,
																])

		cursor_mysql.execute('UPDATE livro SET '
								+ 'encerrado = true '
							+ 'WHERE '
								+ 'fk_setor = %s '
									+ 'AND '
								+ 'tipo = %s '
									+ 'AND '
								+ 'ano = %s '
									+ 'AND '
								+ 'volume = %s', [
													setor[0].id,
													tipo,
													ano,
													volume - 1,
													])

		cursor_postgresql.execute('INSERT INTO livro '
									+ '(fk_setor, tipo, ano, volume, encerrado) '
								+ 'VALUES '
									+ '(%s, %s, %s, %s, 0)', [
																	setor[0].id,
																	tipo,
																	ano,
																	volume,
																	])

		cursor_postgresql.execute('UPDATE livro SET '
									+ 'encerrado = 1 '
								+ 'WHERE '
									+ 'fk_setor = %s '
										+ 'AND '
									+ 'tipo = %s '
										+ 'AND '
									+ 'ano = %s '
										+ 'AND '
									+ 'volume = %s', [
														setor[0].id,
														tipo,
														ano,
														volume - 1,
														])

		messages.add_message(request, messages.SUCCESS, "Protocolo cadastrado com sucesso")
		return redirect(reverse('inout:novo_protocolo'))

	else:
		messages.add_message(request, messages.ERROR, "Preencha todos os campos")
		return redirect(reverse('inout:novo_protocolo'))

@login_required
def lista_protocolos_externos(request):
	lotacao_user = Lotacao.objects.using('default').raw('SELECT * FROM lotacao WHERE fk_user = %s', [request.user.id])
	livros_de_protocolo = Livro.objects.using('default').raw('SELECT * FROM livro WHERE fk_setor = %s AND tipo = 1', [lotacao_user[0].fk_setor.id])

	context = {
		'titulo': "Protocolos externos",
		'livro_list': livros_de_protocolo,
	}

	return render(request, 'inout/lista_protocolos.html', context)

@login_required
def lista_protocolos_internos(request):
	lotacao_user = Lotacao.objects.using('default').raw('SELECT * FROM lotacao WHERE fk_user = %s', [request.user.id])
	livros_de_protocolo = Livro.objects.using('default').raw('SELECT * FROM livro WHERE fk_setor = %s AND tipo = 2', [lotacao_user[0].fk_setor.id])

	context = {
		'titulo': "Protocolos internos",
		'livro_list': livros_de_protocolo,
	}

	return render(request, 'inout/lista_protocolos.html', context)

@login_required
def lista_protocolos_usf(request):
	lotacao_user = Lotacao.objects.using('default').raw('SELECT * FROM lotacao WHERE fk_user = %s', [request.user.id])
	livros_de_protocolo = Livro.objects.using('default').raw('SELECT * FROM livro WHERE fk_setor = %s AND tipo = 3', [lotacao_user[0].fk_setor.id])

	context = {
		'titulo': "Protocolos USF",
		'livro_list': livros_de_protocolo,
	}

	return render(request, 'inout/lista_protocolos.html', context)

#View Generica
class lista_protocolos(ListView):
	model = Livro
	template_name = 'inout/lista_protocolos.html'

@login_required
def protocolar_documento(request):
	#//documentos_disponiveis = Documento.objects.raw('SELECT * FROM documento WHERE documento.id NOT IN (SELECT DISTINCT fk_documento FROM protocolo)')
	#//documentos_disponiveis = Documento.objects.raw('SELECT * FROM documento WHERE NOT EXISTS (SELECT DISTINCT fk_documento FROM protocolo WHERE protocolo.fk_documento = documento.id)')
	#//lista_de_documentos = Documento.objects.raw('SELECT * FROM documento INNER JOIN lotacao ON lotacao.fk_user = documento.fk_user WHERE fk_setor = %s', [lotacao_user[0].fk_setor.id])
	lotacao_user = Lotacao.objects.using('default').raw('SELECT * FROM lotacao WHERE fk_user = %s', [request.user.id])
	documentos_disponiveis = Documento.objects.using('default').raw('SELECT doc.* FROM documento doc '
																	+ 'LEFT OUTER JOIN protocolo prot ON doc.id = prot.fk_documento '
																	+ 'INNER JOIN lotacao ON lotacao.fk_user = doc.fk_user '
																	+ 'WHERE '
																		+ 'fk_setor = %s '
																			+ 'AND '
																		+ 'prot.fk_documento IS null', [
																										lotacao_user[0].fk_setor.id
																										])
	livros_de_protocolo = Livro.objects.using('default').raw('SELECT * FROM livro WHERE fk_setor = %s AND encerrado = false', [lotacao_user[0].fk_setor.id])
	lotacao_do_usuario_logado = Lotacao.objects.using('default').raw('SELECT * FROM lotacao WHERE fk_user = %s', [request.user.id])
	lista_de_setores = Setor.objects.using('default').raw('SELECT * FROM setor WHERE fk_orgao = %s', [lotacao_do_usuario_logado[0].fk_setor.fk_orgao.id])

	context = {
		'titulo': "Protocolar documento",
		'documentos_disponiveis': documentos_disponiveis,
		'livros_de_protocolo': livros_de_protocolo,
		'lista_de_setores': lista_de_setores,
	}

	return render(request, 'inout/protocolar_documento.html', context)

@login_required
def salvar_protocolo_documento(request):
	lotacao_do_usuario_logado = Lotacao.objects.using('default').raw('SELECT * FROM lotacao WHERE fk_user = %s', [request.user.id])
	numero_pagina = request.POST.get("pagina", False)
	pagina = Pagina.objects.using('default').raw('SELECT * FROM pagina WHERE numero = %s AND fk_livro = %s', [numero_pagina, request.POST.get("livro", False)])
	
	if pagina:
		pagina_id_mysql = pagina[0].id
		pagina_id_postgresql = pagina[0].id

	else:
		cursor_mysql.execute('INSERT INTO pagina '
								+ '(fk_livro, numero) '
							+ 'VALUES '
								+ '(%s, %s)', [
												request.POST.get("livro", False),
												numero_pagina
												])

		cursor_mysql.execute('SELECT MAX(id) FROM pagina')
		pagina_id_mysql = cursor_mysql.fetchone()[0]

		cursor_postgresql.execute('INSERT INTO pagina '
									+ '(fk_livro, numero) '
								+ 'VALUES '
									+ '(%s, %s)', [
													request.POST.get("livro", False),
													numero_pagina
													])

		cursor_postgresql.execute('SELECT MAX(id) FROM pagina')
		pagina_id_postgresql = cursor_postgresql.fetchone()[0]

	cursor_mysql.execute('INSERT INTO protocolo '
							+ '(fk_documento, fk_setor_origem, fk_setor_destino, fk_pagina, entregue) '
						+ 'VALUES '
							+ '(%s, %s, %s, %s, false)', [
															request.POST.get("documento", False),
															lotacao_do_usuario_logado[0].fk_setor.id,
															request.POST.get("setor_destino", False),
															pagina_id_mysql,
															])

	cursor_postgresql.execute('INSERT INTO protocolo '
								+ '(fk_documento, fk_setor_origem, fk_setor_destino, fk_pagina, entregue) '
							+ 'VALUES '
								+ '(%s, %s, %s, %s, false)', [
																request.POST.get("documento", False),
																lotacao_do_usuario_logado[0].fk_setor.id,
																request.POST.get("setor_destino", False),
																pagina_id_postgresql,
																])

	return redirect(reverse('inout:index'))

@login_required
def busca_numero_documento(request):
	numero_do_documento = request.POST.get('numero_do_documento', False)
	resultado_da_busca = Documento.objects.using('default').raw('SELECT * FROM documento WHERE numero LIKE %s', ['%' + numero_do_documento + '%'])

	context = {
		'titulo': 'Resultado da busca por',
		'lista_de_documentos': resultado_da_busca,
	}

	return render(request, 'inout/listardocumentos.html', context)

def error_404_view(request, exception):
    
    return render(request,'inout/404.html')

def error_500_view(request):
    
    return render(request,'inout/500.html')


#####* FALTA IMPLEMENTAR #####


#TODO Busca avançada de documento, com uso de filtros
@login_required
def busca_avancada(request):

	context = {
		'titulo': "Busca avançada",
	}

	return render(request, 'inout/busca_avancada.html', context)


#####* DADOS DOS GRÁFICOS - criar arquivo


class chart_data_linha(APIView):
	authentication_classes = []
	permission_classes = []

	def get(self, request, format=None):

		data_de_hoje = datetime.date.today()
		documentosCadastrados = []

		for i in range(-11, 0, 1):
			documentosCadastrados.append(Documento.objects.filter(data_de_recebimento__month = (data_de_hoje + relativedelta(months = i)).month).count())

		documentosCadastrados.append(len(Documento.objects.filter(data_de_recebimento__month = data_de_hoje.month)))
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
			len(Documento.objects.filter(tipo = 9)),
			len(Documento.objects.filter(tipo = 10)),
			len(Documento.objects.filter(tipo = 5)),
			len(Documento.objects.filter(tipo = 6)),
			len(Documento.objects.exclude(tipo = 9).exclude(tipo = 10).exclude(tipo = 5).exclude(tipo = 6)),
			#//len(Documento.objects.filter(tipo_de_documento = "Requerimento")),
			#//len(Documento.objects.filter(tipo_de_documento = "Mandado de Intimação")),
			#//len(Documento.objects.filter(tipo_de_documento = "Notificação")),
			#//len(Documento.objects.filter(tipo_de_documento = "Documento")),
		]

		tiposDeDocumento = [
			"Ofício",
			"Ofício Circular",
			"Memorando",
			"Memorando Circular",
			"Outros",
			#//"Requerimento",
			#//"Mandado de Intimação",
			#//"Notificação",
			#//"Documento",
		]

		dados_grafico_pie = {
			'quantidadeTipoDocumento': quantidadeTipoDocumento,
			'tiposDeDocumento': tiposDeDocumento,
		}

		return Response(dados_grafico_pie)


#####* FUNÇÕES - criar arquivo


def prazos_do_dia():
	lista_de_documentos = Documento.objects.using('default').raw('SELECT * FROM documento INNER JOIN prazo ON prazo.fk_documento = documento.id WHERE prazo.vencimento = %s', [datetime.date.today()])
	#lista_de_documentos = Documento.objects.filter(prazo__vencimento = datetime.date.today())

	return lista_de_documentos

#Retorna todos os documentos cadastrados no dia de hoje
def documentos_do_dia():
	feitos_hoje = Documento.objects.using('default').raw('SELECT * FROM documento WHERE documento.data_de_recebimento = %s', [datetime.date.today()])
	#feitos_hoje = Documento.objects.filter(data_de_recebimento__day = datetime.date.today().day)

	return feitos_hoje

#Retorna todos os documentos cadastrados na semana atual
def documentos_da_semana():
	feitos_semana = Documento.objects.using('default').raw('SELECT * FROM documento WHERE WEEK(data_de_recebimento) = WEEK(%s)', [datetime.date.today()])
	#feitos_semana = Documento.objects.raw('SELECT * FROM documento WHERE WEEK(data_de_recebimento) = %s', [datetime.date.today().isocalendar()[1]])
	#feitos_semana = Documento.objects.filter(data_de_recebimento__week = datetime.date.today().isocalendar()[1])

	return feitos_semana

#Retorna todos os documentos cadastrados no mês atual
def documentos_do_mes():
	feitos_mes = Documento.objects.using('default').raw('SELECT * FROM documento WHERE MONTH(data_de_recebimento) = %s', [datetime.date.today().month])
	#feitos_mes = Documento.objects.filter(data_de_recebimento__month = datetime.date.today().month)

	return feitos_mes

def retorna_mes(mes_numero):
	lista = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

	return lista[mes_numero - 1]