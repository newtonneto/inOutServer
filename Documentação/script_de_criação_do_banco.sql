CREATE TABLE User(
	id INTEGER NOT NULL,
    username VARCHAR(20) NOT NULL,
    password VARCHAR(32) NOT NULL,
    first_name VARCHAR(15),
    last_name VARCHAR(50),
    email VARCHAR(50),
    grupo VARCHAR(15),
    PRIMARY KEY(id)
);

CREATE TABLE Processo(
	id INTEGER NOT NULL,
    numero VARCHAR(21) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE Documento(
	id INTEGER NOT NULL,
    fk_user INTEGER NOT NULL,
    fk_processo INTEGER,
	data_de_recebimento DATE NOT NULL,
    tipo INTEGER NOT NULL DEFAULT 10,
    numero VARCHAR(30) NOT NULL,
    emissor VARCHAR(50) NOT NULL,
    assunto VARCHAR(1000) NOT NULL,
    despacho VARCHAR(200) NOT NULL,
    entrega_pessoal TINYINT NOT NULL DEFAULT false,
    PRIMARY KEY(id),
    FOREIGN KEY(fk_user) REFERENCES User(id),
    FOREIGN KEY(fk_processo) REFERENCES Processo(id)
);

CREATE TABLE Prazo(
	id INTEGER NOT NULL,
    fk_documento INTEGER NOT NULL,
    tipo INTEGER NOT NULL,
    vencimento DATETIME NOT NULL,
    encerrado TINYINT NOT NULL DEFAULT false,
    dilacao TINYINT NOT NULL DEFAULT false,
    quantidade_de_dilacoes INTEGER DEFAULT 0,
    PRIMARY KEY(id),
    FOREIGN KEY(fk_documento) REFERENCES Documento(id)
);

CREATE TABLE Orgao(
	id INTEGER NOT NULL,
	nome VARCHAR(50) NOT NULL,
	sigla VARCHAR(10) NOT NULL,
	esfera INTEGER NOT NULL,
	municipio VARCHAR(32) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE Setor(
	id INTEGER NOT NULL,
    fk_orgao INTEGER NOT NULL,
    nome INTEGER NOT NULL,
    ativo TINYINT NOT NULL DEFAULT true,
    PRIMARY KEY(id),
    FOREIGN KEY(fk_orgao) REFERENCES Orgao(id)
);

CREATE TABLE Lotacao(
	id INTEGER NOT NULL,
    fk_user INTEGER NOT NULL,
    fk_setor INTEGER NOT NULL,
    cargo INTEGER NOT NULL,
    entrada DATE NOT NULL,
    saida DATE,
    FOREIGN KEY(fk_user) REFERENCES User(id),
    FOREIGN KEY(fk_setor) REFERENCES Setor(id)
);

CREATE TABLE Livro(
	id INTEGER NOT NULL,
    fk_setor INTEGER NOT NULL,
    tipo INTEGER NOT NULL DEFAULT 2,
    ano INTEGER NOT NULL,
    volume INTEGER NOT NULL DEFAULT 1,
    encerrado TINYINT DEFAULT false,
    PRIMARY KEY(id),
    FOREIGN KEY(fk_setor) REFERENCES Setor(id)
);

CREATE TABLE Pagina(
	id INTEGER NOT NULL,
    fk_livro INTEGER NOT NULL,
    numero INTEGER NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(fk_livro) REFERENCES Livro(id)
);

CREATE TABLE Protocolo(
	id INTEGER NOT NULL,
    fk_documento INTEGER NOT NULL,
    fk_setor_origem INTEGER NOT NULL,
    fk_setor_destino INTEGER NOT NULL,
    fk_pagina INTEGER NOT NULL,
    entregue TINYINT NOT NULL,
    data_da_entrega DATE,
    PRIMARY KEY(id),
    FOREIGN KEY(fk_documento) REFERENCES Documento(id),
    FOREIGN KEY(fk_setor_origem) REFERENCES Setor(id),
    FOREIGN KEY(fk_setor_destino) REFERENCES Setor(id),
    FOREIGN KEY(fk_pagina) REFERENCES Pagina(id)
);