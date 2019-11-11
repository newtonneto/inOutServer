from django.shortcuts import render
from inout.models import Lotacao, Orgao, Setor
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.
def cadastro_usuario(request):
    contexto = {
		'titulo': "Cadastrar novo usuário",
        'select': Lotacao(),
        'lista_de_orgaos': Orgao.objects.all(),
	}

    return render(request, 'usuario/cadastro_usuario.html', contexto)

def salva_usuario(request):
    user = User.objects.create_user(request.POST.get('username', False), password = request.POST.get('password', False), email = request.POST.get('email', False))
    user.first_name = request.POST.get('first_name', False)
    user.last_name = request.POST.get('last_name', False)
    user.save()

    setor = Setor()
    setor.orgao = Orgao.objects.get(pk = request.POST.get('orgao', False))
    setor.nome = request.POST.get('setor', False)
    setor.save()

    lotacao = Lotacao()
    lotacao.cargo = request.POST.get('cargo', False)
    lotacao.usuario = user
    lotacao.setor = setor
    lotacao.save()

    return render(request, 'registration/login.html')

@login_required
def lista_usuarios(request):

	context = {
		'titulo': "Lista de usuários cadastrados",
	}

	return render(request, 'usuario/lista_usuarios.html', context)