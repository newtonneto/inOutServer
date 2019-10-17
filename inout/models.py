from django.db import models
from django.contrib.auth.models import User

class Processo(models.Model):
	numero = models.CharField(max_length = 30)

	def __str__(self):
		return self.numero

class Documento(models.Model):
	usuario = models.ForeignKey(User, on_delete = models.PROTECT)
	processo = models.ForeignKey(Processo, on_delete = models.SET_NULL, null = True)
	data_de_recebimento = models.DateTimeField('Data de Entrada')
	tipos_choices = [
		(0, 'Carta'),
		(1, 'Convite'),
		(2, 'Documento'),
		(3, 'Email'),
		(4, 'Mandado de Intimação'),
		(5, 'Memorando'),
		(6, 'Memorando Circular'),
		(7, 'Movimentação da Solicitação'),
		(8, 'Notificação'),
		(9, 'Ofício'),
		(10, 'Ofício Circular'),
		(11, 'Requerimento'),
		(12, 'Outros'),
	]
	tipo = models.IntegerField(choices = tipos_choices, default = 9)
	numero = models.CharField(max_length = 30)
	emissor = models.CharField(max_length = 150)
	assunto = models.CharField(max_length = 1000)
	despacho = models.CharField(max_length = 200)

	def __str__(self):
		return "{} {} - {}".format(self.tipo, self.numero, self.emissor)

	def tipo_do_documento(self):
		return self.tipos_choices[self.tipo][1]

class Prazo(models.Model):
	documento = models.ForeignKey(Documento, on_delete = models.CASCADE)
	tipo = models.CharField(max_length = 20)
	vencimento = models.DateTimeField('Prazo')
	encerrado = models.BooleanField(default = False)

	def __str__(self):
		return "{} {}".format(self.tipo, self.vencimento)

class Orgao(models.Model):
	nome = models.CharField(max_length=50)

	def __str__(self):
		return self.nome

class Setor(models.Model):
	orgao = models.ForeignKey(Orgao, on_delete = models.PROTECT)
	nome = models.CharField(max_length = 50)

	def __str__(self):
		return self.nome

class Livro(models.Model):
	setor = models.ForeignKey(Setor, on_delete = models.PROTECT)
	tipo = models.CharField(max_length = 10)
	ano = models.DateTimeField('Ano do Livro')
	volume = models.IntegerField()

	def __str__(self):
		return "Protocolo {} {} Volume {}".format(self.tipo, self.ano, self.volume)

class Pagina(models.Model):
	livro = models.ForeignKey(Livro, on_delete = models.PROTECT)
	numero = models.IntegerField()

	def __str__(self):
		return self.numero

class Protocolo(models.Model):
	documento = models.ForeignKey(Documento, on_delete = models.PROTECT)
	setor = models.ForeignKey(Setor, on_delete = models.PROTECT)
	pagina = models.ForeignKey(Pagina, on_delete = models.PROTECT)
	entregue = models.BooleanField(default = False)
