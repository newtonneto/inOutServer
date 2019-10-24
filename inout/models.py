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
		(1, 'Carta'),
		(2, 'Convite'),
		(3, 'Documento'),
		(4, 'Email'),
		(5, 'Mandado de Intimação'),
		(6, 'Memorando'),
		(7, 'Memorando Circular'),
		(8, 'Movimentação da Solicitação'),
		(9, 'Notificação'),
		(10, 'Ofício'),
		(11, 'Ofício Circular'),
		(12, 'Requerimento'),
		(13, 'Outro'),
	]
	tipo = models.IntegerField(choices = tipos_choices, default = 9)
	numero = models.CharField(max_length = 30)
	emissor = models.CharField(max_length = 150)
	assunto = models.CharField(max_length = 1000)
	despacho = models.CharField(max_length = 200)
	entrega_pessoal = models.BooleanField(default = False)

	def __str__(self):
		return "{} {} - {}".format(self.tipo, self.numero, self.emissor)

	def tipo_do_documento(self):
		return self.tipos_choices[self.tipo][1]

class Prazo(models.Model):
	documento = models.ForeignKey(Documento, on_delete = models.CASCADE)
	tipos_choices = [
		(1, 'Audiência'),
		(2, 'Audiência Pública'),
		(3, 'Evento'),
		(4, 'Resposta'),
		(5, 'Reunião'),
		(6, 'Outro'),
	]
	tipo = models.IntegerField(choices = tipos_choices, default = 4)
	vencimento = models.DateTimeField('Prazo')
	encerrado = models.BooleanField(default = False)
	dilacao = models.BooleanField(default = False)
	quantidade_de_dilacoes = models.IntegerField(default = 0)

	def __str__(self):
		return "{} {}".format(self.tipo, self.vencimento)

class Orgao(models.Model):
	nome = models.CharField(max_length=50)

	def __str__(self):
		return self.nome

class Setor(models.Model):
	orgao = models.ForeignKey(Orgao, on_delete = models.PROTECT)
	nome_choices = [
		(1, 'AJUR'),
		(2, 'APOIO AO GABINETE'),
		(3, 'ASSCOM'),
		(4, 'ASSTEC'),
		(5, 'ATENDIMENTO'),
		(6, 'DAG'),
		(7, 'DASA'),
		(8, 'DCRA'),
		(9, 'DFUA'),
		(10, 'DGSIG'),
		(11, 'DLOS'),
		(12, 'GABINETE'),
		(13, 'INFORMATICA'),
		(14, 'OUVIDORIA'),
		(15, 'PROTOCOLO'),
		(16, 'RH'),
		(17, 'SAAG'),
		(18, 'SAFL'),
		(19, 'SAIPUA'),
		(20, 'SANBIO'),
		(21, 'SCALA'),
		(22, 'SDI'),
		(23, 'SGCT'),
		(24, 'SGFA'),
		(25, 'SGFU'),
		(26, 'SJPI'),
		(27, 'SLOPR'),
		(28, 'SLOPU'),
		(29, 'SLS'),
		(30, 'SPASO'),
		(31, 'SPATS'),
		(32, 'SPPUA'),
		(33, 'SZL'),
		(34, 'SZN'),
		(35, 'SZO'),
		(36, 'SZS'),
		(37, 'USF'),
	]
	nome = models.IntegerField(choices = nome_choices)
	ativo = models.BooleanField(default = True)

	def __str__(self):
		return self.nome

class Livro(models.Model):
	setor = models.ForeignKey(Setor, on_delete = models.PROTECT)
	tipos_choices = [
		(1, "Interno"),
		(2, "Externo"),
		(3, "USF"),
	]
	tipo = models.IntegerField(choices = tipos_choices, default = 1)
	ano = models.DateTimeField('Ano do Livro')
	volume = models.IntegerField()
	encerrado = models.BooleanField(default = False)

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
	data_da_entrega = models.DateTimeField('Data da Entrega', null = True)