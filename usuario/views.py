from django.shortcuts import render

# Create your views here.
def cadastro_usuario(request):
    contexto = {
		'titulo': "Cadastrar novo usuário",
	}

    return render(request, 'usuario/cadastro_usuario.html', contexto)