from django.db import models

# Create your models here.
class Usuario(models.Model):
	nome_de_usuario = models.CharField(max_length = 20)
	senha = models.CharField(max_length = 16)

class Documento(models.Model):
	data_de_entrada = models.DateTimeField('Data de Entrada')
	tipo_de_documento = models.CharField(max_length = 30)
	numero_do_documento = models.CharField(max_length = 30)
	orgao_expedidor_do_documento = models.CharField(max_length = 150)
	assunto_do_documento = models.CharField(max_length = 1000)
	despacho_do_documento = models.CharField(max_length = 200)
	numero_do_processo = models.CharField(max_length = 30)

	def __str__(self):
		return self.numero_do_documento

class Prazo(models.Model):
	documento = models.ForeignKey(Documento, on_delete = models.CASCADE)
	tipo_de_prazo = models.CharField(max_length = 20)
	data_do_prazo = models.DateTimeField('Prazo')