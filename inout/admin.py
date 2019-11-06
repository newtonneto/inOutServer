from django.contrib import admin
from .models import Documento, Processo, Prazo, Orgao

# Register your models here.
admin.site.register(Documento)
admin.site.register(Processo)
admin.site.register(Prazo)
admin.site.register(Orgao)
