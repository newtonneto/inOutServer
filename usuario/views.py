from django.shortcuts import render, redirect
from inout.models import Lotacao, Orgao, Setor
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import timedelta
from django.db import connections
import datetime

cursor_mysql = connections['default'].cursor()
cursor_postgresql = connections['postgresql'].cursor()

# Create your views here.
def cadastro_usuario(request):
    lista_de_setores = Setor.objects.raw('SELECT * FROM setor')

    contexto = {
		'titulo': "Cadastrar novo usuário",
        'select': Lotacao(),
        'lista_de_orgaos': Orgao.objects.all(),
        'lista_de_setores': lista_de_setores,
	}

    return render(request, 'usuario/cadastro_usuario.html', contexto)

def salva_usuario(request):
    user = User.objects.db_manager('default').create_user(request.POST.get('username', False), password = request.POST.get('password', False), email = request.POST.get('email', False))
    user.first_name = request.POST.get('first_name', False)
    user.last_name = request.POST.get('last_name', False)
    user.save()

    user_postgresql = User.objects.db_manager('postgresql').create_user(request.POST.get('username', False), password = request.POST.get('password', False), email = request.POST.get('email', False))
    user_postgresql.first_name = request.POST.get('first_name', False)
    user_postgresql.last_name = request.POST.get('last_name', False)
    user_postgresql.save()

    """ setor = Setor()
    setor.orgao = Orgao.objects.get(pk = request.POST.get('orgao', False))
    setor.nome = request.POST.get('setor', False)
    setor.save()

    lotacao = Lotacao()
    lotacao.cargo = request.POST.get('cargo', False)
    lotacao.usuario = user
    lotacao.setor = setor
    lotacao.save() """

    setor = Setor.objects.using('default').raw('SELECT * FROM setor WHERE id = %s', [request.POST.get('setor', False)])
    cargo = request.POST.get('cargo', False)

    if setor and cargo:
        #with connection.cursor() as cursor:
        cursor_mysql.execute('INSERT INTO lotacao '
                                + '(fk_user, fk_setor, cargo, entrada) '
                            + 'VALUES '
                                + '(%s, %s, %s, %s)', [
                                                        user.id,
                                                        request.POST.get('setor', False),
                                                        cargo,
                                                        datetime.date.today(),
                                                        ])

        cursor_postgresql.execute('INSERT INTO lotacao '
                                    + '(fk_user, fk_setor, cargo, entrada) '
                                + 'VALUES '
                                    + '(%s, %s, %s, %s)', [
                                                            user.id,
                                                            request.POST.get('setor', False),
                                                            cargo,
                                                            datetime.date.today(),
                                                            ])


    
    else:
        messages.add_message(request, messages.ERROR, "Preencha todos os campos")

        return redirect(reverse('registration:cadastro_usuario'))

    messages.add_message(request, messages.SUCCESS, "Usuário cadastrado com sucesso")
    
    login(request, user)

    return redirect(reverse('inout:index'))

@login_required
def lista_usuarios(request):

	context = {
		'titulo': "Lista de usuários cadastrados",
	}

	return render(request, 'usuario/lista_usuarios.html', context)