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
    user_id INTEGER NOT NULL,
    processo_id INTEGER,
	data_de_recebimento DATE NOT NULL,
    tipo INTEGER NOT NULL,
    numero VARCHAR(30) NOT NULL,
    emissor VARCHAR(50) NOT NULL,
    assunto VARCHAR(1000) NOT NULL,
    despacho VARCHAR(200) NOT NULL,
    entrega_pessoal TINYINT NOT NULL DEFAULT false,
    PRIMARY KEY(id),
    FOREIGN KEY(user_id) REFERENCES User(id),
    FOREIGN KEY(processo_id) REFERENCES Processo(id)
);

CREATE TABLE Prazo(
	id INTEGER NOT NULL,
    documento_id INTEGER NOT NULL,
    tipo INTEGER NOT NULL,
    vencimento DATETIME NOT NULL,
    encerrado TINYINT NOT NULL,
    dilacao TINYINT NOT NULL,
    quantidade_de_dilacoes INTEGER,
    PRIMARY KEY(id),
    FOREIGN KEY(documento_id) REFERENCES Documento(id)
);

CREATE TABLE Orgao(
	id INTEGER NOT NULL,
	nome VARCHAR(50) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE Setor(
	id INTEGER NOT NULL,
    orgao_id INTEGER NOT NULL,
    nome INTEGER NOT NULL,
    ativo TINYINT NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(orgao_id) REFERENCES Orgao(id)
);

CREATE TABLE Livro(
	id INTEGER NOT NULL,
    setor_id INTEGER NOT NULL,
    tipo INTEGER NOT NULL,
    ano DATE NOT NULL,
    volume INTEGER NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(setor_id) REFERENCES Setor(id)
);

CREATE TABLE Pagina(
	id INTEGER NOT NULL,
    livro_id INTEGER NOT NULL,
    numero INTEGER NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(livro_id) REFERENCES Livro(id)
);

CREATE TABLE Protocolo(
	id INTEGER NOT NULL,
    documento_id INTEGER NOT NULL,
    setor_id INTEGER NOT NULL,
    pagina_id INTEGER NOT NULL,
    entregue TINYINT NOT NULL,
    data_da_entrega DATE NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(documento_id) REFERENCES Documento(id),
    FOREIGN KEY(setor_id) REFERENCES Setor(id),
    FOREIGN KEY(pagina_id) REFERENCES Pagina(id)
);