# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Documento(models.Model):
    id = models.AutoField(primary_key=True)
    fk_user = models.ForeignKey(User, models.DO_NOTHING, db_column='fk_user')
    fk_processo = models.ForeignKey('Processo', models.DO_NOTHING, db_column='fk_processo', blank=True, null=True)
    data_de_recebimento = models.DateField()
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
    numero = models.CharField(max_length=30)
    emissor = models.CharField(max_length=50)
    assunto = models.CharField(max_length=1000)
    despacho = models.CharField(max_length=200)
    entrega_pessoal = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "{} {} - {}".format(self.tipo, self.numero, self.emissor)
    
    def tipo_do_documento(self):
        return self.tipos_choices[self.tipo][1]
    
    class Meta:
        db_table = 'documento'

class Livro(models.Model):
    id = models.IntegerField(primary_key=True)
    fk_setor = models.ForeignKey('Setor', models.DO_NOTHING, db_column='fk_setor')
    tipos_choices = [
		(1, "Externo"),
		(2, "Interno"),
		(3, "USF"),
	]
    tipo = models.IntegerField(choices = tipos_choices, default = 2)
    ano = models.IntegerField()
    volume = models.IntegerField()
    encerrado = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "Protocolo {} {} Volume {}".format(self.tipo, self.ano, self.volume)
    
    class Meta:
        db_table = 'livro'


class Lotacao(models.Model):
    id = models.IntegerField(primary_key=True)
    fk_user = models.ForeignKey(User, models.DO_NOTHING, db_column='fk_user')
    fk_setor = models.ForeignKey('Setor', models.DO_NOTHING, db_column='fk_setor')
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
    entrada = models.DateField()
    saida = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'lotacao'


class Orgao(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)
    sigla = models.CharField(max_length=10)
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
    estado = models.IntegerField(choices = estado_choices, default=20)
    municipio = models.CharField(max_length=32)
    ativo = models.IntegerField(default=1)

    def __str__(self):
        return self.sigla

    class Meta:
        db_table = 'orgao'


class Pagina(models.Model):
    id = models.AutoField(primary_key=True)
    fk_livro = models.ForeignKey(Livro, models.DO_NOTHING, db_column='fk_livro')
    numero = models.IntegerField()

    def __str__(self):
        return self.numero

    class Meta:
        db_table = 'pagina'


class Prazo(models.Model):
    id = models.AutoField(primary_key=True)
    fk_documento = models.ForeignKey(Documento, models.DO_NOTHING, db_column='fk_documento')
    tipo = models.IntegerField()
    vencimento = models.DateField()
    encerrado = models.IntegerField(blank=True, null=True)
    dilacao = models.IntegerField(blank=True, null=True)
    quantidade_de_dilacoes = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "{} {}".format(self.tipo, self.vencimento)

    class Meta:
        db_table = 'prazo'


class Processo(models.Model):
    id = models.AutoField(primary_key=True)
    numero = models.CharField(max_length=21)

    def __str__(self):
        return self.numero

    class Meta:
        db_table = 'processo'


class Protocolo(models.Model):
    id = models.AutoField(primary_key=True)
    fk_documento = models.ForeignKey(Documento, models.DO_NOTHING, db_column='fk_documento')
    fk_setor_origem = models.ForeignKey('Setor', models.DO_NOTHING, db_column='fk_setor_origem', related_name = 'setor_de_origem')
    fk_setor_destino = models.ForeignKey('Setor', models.DO_NOTHING, db_column='fk_setor_destino', related_name = 'setor_de_destino')
    fk_pagina = models.ForeignKey(Pagina, models.DO_NOTHING, db_column='fk_pagina')
    entregue = models.IntegerField()
    data_da_entrega = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'protocolo'


class Setor(models.Model):
    id = models.AutoField(primary_key=True)
    fk_orgao = models.ForeignKey(Orgao, models.DO_NOTHING, db_column='fk_orgao')
    nome = models.CharField(max_length=50)
    sigla = models.CharField(max_length=10)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'setor'