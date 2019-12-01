# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Documento(models.Model):
    data_de_recebimento = models.DateField()
    tipo = models.IntegerField()
    numero = models.CharField(max_length=30)
    emissor = models.CharField(max_length=50)
    assunto = models.CharField(max_length=1000)
    despacho = models.CharField(max_length=200)
    entrega_pessoal = models.IntegerField()
    fk_processo = models.ForeignKey('Processo', models.DO_NOTHING, db_column='fk_processo', blank=True, null=True)
    fk_user = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='fk_user')
    pdf = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'documento'


class Livro(models.Model):
    tipo = models.IntegerField()
    ano = models.IntegerField()
    volume = models.IntegerField()
    encerrado = models.IntegerField(blank=True, null=True)
    fk_setor = models.ForeignKey('Setor', models.DO_NOTHING, db_column='fk_setor')

    class Meta:
        managed = False
        db_table = 'livro'


class Lotacao(models.Model):
    cargo = models.IntegerField()
    entrada = models.DateField()
    saida = models.DateField(blank=True, null=True)
    fk_setor = models.ForeignKey('Setor', models.DO_NOTHING, db_column='fk_setor')
    fk_user = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='fk_user')

    class Meta:
        managed = False
        db_table = 'lotacao'


class Orgao(models.Model):
    nome = models.CharField(max_length=50)
    sigla = models.CharField(max_length=10)
    esfera = models.IntegerField()
    estado = models.IntegerField()
    municipio = models.CharField(max_length=32)
    ativo = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'orgao'


class Pagina(models.Model):
    numero = models.IntegerField()
    fk_livro = models.ForeignKey(Livro, models.DO_NOTHING, db_column='fk_livro')

    class Meta:
        managed = False
        db_table = 'pagina'


class Prazo(models.Model):
    tipo = models.IntegerField()
    vencimento = models.DateField()
    encerrado = models.IntegerField()
    dilacao = models.IntegerField()
    quantidade_de_dilacoes = models.IntegerField(blank=True, null=True)
    fk_documento = models.ForeignKey(Documento, models.DO_NOTHING, db_column='fk_documento')

    class Meta:
        managed = False
        db_table = 'prazo'


class Processo(models.Model):
    numero = models.CharField(max_length=21)

    class Meta:
        managed = False
        db_table = 'processo'


class Protocolo(models.Model):
    entregue = models.IntegerField()
    data_da_entrega = models.DateField(blank=True, null=True)
    fk_documento = models.ForeignKey(Documento, models.DO_NOTHING, db_column='fk_documento')
    fk_pagina = models.ForeignKey(Pagina, models.DO_NOTHING, db_column='fk_pagina')
    fk_setor_destino = models.ForeignKey('Setor', models.DO_NOTHING, db_column='fk_setor_destino')
    fk_setor_origem = models.ForeignKey('Setor', models.DO_NOTHING, db_column='fk_setor_origem')

    class Meta:
        managed = False
        db_table = 'protocolo'


class Setor(models.Model):
    nome = models.CharField(max_length=50)
    sigla = models.CharField(max_length=10)
    ativo = models.IntegerField()
    fk_orgao = models.ForeignKey(Orgao, models.DO_NOTHING, db_column='fk_orgao')

    class Meta:
        managed = False
        db_table = 'setor'
