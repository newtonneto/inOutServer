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
    tipo = models.IntegerField()
    numero = models.CharField(max_length=30)
    emissor = models.CharField(max_length=50)
    assunto = models.CharField(max_length=1000)
    despacho = models.CharField(max_length=200)
    entrega_pessoal = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'documento'


class Livro(models.Model):
    id = models.IntegerField(primary_key=True)
    fk_setor = models.ForeignKey('Setor', models.DO_NOTHING, db_column='fk_setor')
    tipo = models.IntegerField()
    ano = models.IntegerField()
    volume = models.IntegerField()
    encerrado = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'livro'


class Lotacao(models.Model):
    id = models.IntegerField(primary_key=True)
    fk_user = models.ForeignKey(User, models.DO_NOTHING, db_column='fk_user')
    fk_setor = models.ForeignKey('Setor', models.DO_NOTHING, db_column='fk_setor')
    cargo = models.IntegerField()
    entrada = models.DateField()
    saida = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'lotacao'


class Orgao(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=50)
    sigla = models.CharField(max_length=10)
    esfera = models.IntegerField()
    municipio = models.CharField(max_length=32)

    class Meta:
        db_table = 'orgao'


class Pagina(models.Model):
    id = models.IntegerField(primary_key=True)
    fk_livro = models.ForeignKey(Livro, models.DO_NOTHING, db_column='fk_livro')
    numero = models.IntegerField()

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

    class Meta:
        db_table = 'prazo'


class Processo(models.Model):
    id = models.AutoField(primary_key=True)
    numero = models.CharField(max_length=21)

    class Meta:
        db_table = 'processo'


class Protocolo(models.Model):
    id = models.IntegerField(primary_key=True)
    fk_documento = models.ForeignKey(Documento, models.DO_NOTHING, db_column='fk_documento')
    fk_setor_origem = models.ForeignKey('Setor', models.DO_NOTHING, db_column='fk_setor_origem', related_name = 'setor_de_origem')
    fk_setor_destino = models.ForeignKey('Setor', models.DO_NOTHING, db_column='fk_setor_destino', related_name = 'setor_de_destino')
    fk_pagina = models.ForeignKey(Pagina, models.DO_NOTHING, db_column='fk_pagina')
    entregue = models.IntegerField()
    data_da_entrega = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'protocolo'


class Setor(models.Model):
    id = models.IntegerField(primary_key=True)
    fk_orgao = models.ForeignKey(Orgao, models.DO_NOTHING, db_column='fk_orgao')
    nome = models.IntegerField()
    ativo = models.IntegerField()

    class Meta:
        db_table = 'setor'