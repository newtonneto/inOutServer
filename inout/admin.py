from django.contrib import admin
from .models import Documento, Processo, Prazo, Orgao, Setor, Livro, Protocolo, Pagina, Lotacao

# Register your models here.
admin.site.register(Documento)
admin.site.register(Processo)
admin.site.register(Prazo)
admin.site.register(Orgao)
admin.site.register(Setor)
admin.site.register(Livro)
admin.site.register(Protocolo)
admin.site.register(Pagina)
admin.site.register(Lotacao)