from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Processo(models.Model):
	numero = models.CharField(max_length = 21)

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
	tipo = models.IntegerField(choices = tipos_choices, default = 10)
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
	nome = models.CharField(max_length = 50)
	sigla = models.CharField(max_length = 10)
	esfera_choices = [
		(1, "Estadual"),
		(2, "Federal"),
		(3, "Municipal"),
	]
	esfera = models.IntegerField(choices = esfera_choices)
	estado_choices = [
		(1, "Acre (AC)"),
		(2, "Alagoas (AL)"),
		(3, "Amapá (AP)"),
		(4, "Amazonas (AM)"),
		(5, "Bahia (BA)"),
		(6, "Ceará (CE)"),
		(7, "Distrito Federal (DF)"),
		(8, "Espírito Santo (ES)"),
		(9, "Goiás (GO)"),
		(10, "Maranhão (MA)"),
		(11, "Mato Grosso (MT)"),
		(12, "Mato Grosso do Sul (MS)"),
		(13, "Minas Gerais (MG)"),
		(14, "Pará (PA)"),
		(15, "Paraíba (PB)"),
		(16, "Paraná (PR)"),
		(17, "Pernambuco (PE)"),
		(18, "Piauí (PI)"),
		(19, "Rio de Janeiro (RJ)"),
		(20, "Rio Grande do Norte (RN)"),
		(21, "Rio Grande do Sul (RS)"),
		(22, "Rondônia (RO)"),
		(23, "Roraima (RR)"),
		(24, "Santa Catarina (SC)"),
		(25, "São Paulo (SP)"),
		(26, "Sergipe (SE)"),
		(27, "Tocantins (TO)"),
	]
	estado = models.IntegerField(choices = estado_choices)
	municipio = models.CharField(max_length = 32)

	def __str__(self):
		return self.sigla

class Setor(models.Model):
	orgao = models.ForeignKey(Orgao, on_delete = models.PROTECT)
	nome = models.CharField(max_length = 50)
	ativo = models.BooleanField(default = True)

	def __str__(self):
		return self.nome

class Lotacao(models.Model):
	usuario = models.ForeignKey(User, on_delete = models.PROTECT)
	setor = models.ForeignKey(Setor, on_delete = models.PROTECT)
	cargo_choices = [
		(1, "Arquiteto"),
		(2, "Assistente Administrativo"),
		(3, "Chefe de Gabinete"),
		(4, "Diretor"),
		(5, "Estagiário"),
		(6, "Fiscal"),
		(7, "Recepcionista"),
		(8, "Secretário"),
		(9, "Técnico em Informática"),
	]
	cargo = models.IntegerField(choices = cargo_choices)
	entrada = models.DateTimeField('Data de entrada na função', auto_now_add = True)
	saida = models.DateTimeField('Data de saída da função', null = True)

class Livro(models.Model):
	setor = models.ForeignKey(Setor, on_delete = models.PROTECT)
	tipos_choices = [
		(1, "Externo"),
		(2, "Interno"),
		(3, "USF"),
	]
	tipo = models.IntegerField(choices = tipos_choices, default = 2)
	ano = models.DateTimeField('Ano do Livro')
	volume = models.IntegerField(default = 1)
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
	#Para utilizar duas chaves estrangeiras pro mesmo modelo é necessário utilizar o parametro 'related_name'
	setor_origem = models.ForeignKey(Setor, related_name = 'setor_de_origem', on_delete = models.PROTECT)
	setor_destino = models.ForeignKey(Setor, related_name = 'setor_de_destino', on_delete = models.PROTECT)
	pagina = models.ForeignKey(Pagina, on_delete = models.PROTECT)
	entregue = models.BooleanField(default = False)
	data_da_entrega = models.DateTimeField('Data da Entrega', null = True)