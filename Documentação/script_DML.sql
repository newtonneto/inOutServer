INSERT INTO user VALUES (1,'newton','123','newton','neto','newton@email.com',NULL);
INSERT INTO user VALUES (2,'joseane','321','joseane','lima','josy@email.com',NULL);
INSERT INTO user VALUES (3,'juliana','213','juliana','medeiros','juh@email.com',NULL);
INSERT INTO user VALUES (4,'lenise','312','lenise','naosei','lili@email.com',NULL);
INSERT INTO user VALUES (5,'nadja','1234','nadja','rafaela','nadja@email.com',NULL);
INSERT INTO user VALUES (6,'thiago','4321','thiago','naosei','thiago@email.com',NULL);
INSERT INTO user VALUES (7,'daniel','1243','daniel','nicolau','daniel@email.com',NULL);
INSERT INTO user VALUES (8,'alessandra','4312','alessandra','condera','alessandra@email.com',NULL);
INSERT INTO user VALUES (9,'ana','1324','ana','carolina','ana@email.com',NULL);
INSERT INTO user VALUES (10,'izolda','4231','izolda','naosei','izolda@email.com',NULL);

INSERT INTO processo VALUES (1,'123456/2019-01');
INSERT INTO processo VALUES (2,'123456/2019-02');
INSERT INTO processo VALUES (3,'123456/2019-03');
INSERT INTO processo VALUES (4,'123456/2019-04');
INSERT INTO processo VALUES (5,'123456/2019-05');
INSERT INTO processo VALUES (6,'123456/2019-06');
INSERT INTO processo VALUES (7,'123456/2019-07');
INSERT INTO processo VALUES (8,'123456/2019-08');
INSERT INTO processo VALUES (9,'123456/2019-09');
INSERT INTO processo VALUES (10,'123456/2019-10');

INSERT INTO documento VALUES (1,1,1,'2019-10-01',10,'001/2019','SEMURB','Expediente Extraordinario','SGFU',0);
INSERT INTO documento VALUES (2,1,2,'2019-10-02',10,'002/2019','SEMPLA','Protocolo Digital','DCRA',0);
INSERT INTO documento VALUES (3,1,3,'2019-10-03',10,'003/2019','IDEMA','Denuncia','SGFA',0);
INSERT INTO documento VALUES (4,1,4,'2019-10-04',1,'004/2019','IPHAN','Reforma do Palacio Felipe Camarão','SAIPUA',0);
INSERT INTO documento VALUES (5,2,5,'2019-10-05',2,'005/2019','MPF','Denuncia','SGFA',0);
INSERT INTO documento VALUES (6,2,6,'2019-10-06',3,'006/2019','PGM','Solicitação de informações','DGSIG',1);
INSERT INTO documento VALUES (7,3,7,'2019-10-07',4,'007/2019','CMG','Prestação de contas','DAG',1);
INSERT INTO documento VALUES (8,3,8,'2019-10-08',5,'008/2019','SEMAD','Contratos de estagio','RH',1);
INSERT INTO documento VALUES (9,4,9,'2019-10-09',6,'009/2019','UFRN','Solicitação de informações','DGSIG',1);
INSERT INTO documento VALUES (10,4,10,'2019-10-10',7,'010/2019','IFRN','Denuncia','SGFA',1);
INSERT INTO documento VALUES (11,1,NULL,'2019-10-10',11,'011/2019','NUPACIV','Certidão Fundiaria','DGSIG',0);

INSERT INTO prazo VALUES (1,1,1,'2019-11-01 00:00:00',0,0,0);
INSERT INTO prazo VALUES (2,1,2,'2019-11-02 00:00:00',1,1,4);
INSERT INTO prazo VALUES (3,1,3,'2019-11-03 00:00:00',0,0,0);
INSERT INTO prazo VALUES (4,2,4,'2019-11-04 00:00:00',1,0,0);
INSERT INTO prazo VALUES (5,2,5,'2019-11-05 00:00:00',0,0,0);
INSERT INTO prazo VALUES (6,2,6,'2019-11-06 00:00:00',1,0,0);
INSERT INTO prazo VALUES (7,3,1,'2019-11-07 00:00:00',0,1,2);
INSERT INTO prazo VALUES (8,3,2,'2019-11-08 00:00:00',1,0,0);
INSERT INTO prazo VALUES (9,3,3,'2019-11-09 00:00:00',0,0,0);
INSERT INTO prazo VALUES (10,4,4,'2019-11-10 00:00:00',1,1,1);

INSERT INTO orgao VALUES (1,'SEMURB');
INSERT INTO orgao VALUES (2,'SEMPLA');
INSERT INTO orgao VALUES (3,'SEMTAS');
INSERT INTO orgao VALUES (4,'SMS');
INSERT INTO orgao VALUES (5,'SMG');
INSERT INTO orgao VALUES (6,'CGM');
INSERT INTO orgao VALUES (7,'PGM');
INSERT INTO orgao VALUES (8,'SEMDES');
INSERT INTO orgao VALUES (9,'SEMOV');
INSERT INTO orgao VALUES (10,'SEMUT');

INSERT INTO setor VALUES (1,1,1,1);
INSERT INTO setor VALUES (2,1,2,1);
INSERT INTO setor VALUES (3,1,3,1);
INSERT INTO setor VALUES (4,1,4,1);
INSERT INTO setor VALUES (5,1,5,1);
INSERT INTO setor VALUES (6,1,6,1);
INSERT INTO setor VALUES (7,1,7,1);
INSERT INTO setor VALUES (8,1,8,1);
INSERT INTO setor VALUES (9,1,9,1);
INSERT INTO setor VALUES (10,1,10,0);

INSERT INTO lotacao VALUES (1,1,2,2,'2019-01-01',NULL);
INSERT INTO lotacao VALUES (2,2,2,2,'2019-01-02',NULL);
INSERT INTO lotacao VALUES (3,3,2,3,'2019-01-03',NULL);
INSERT INTO lotacao VALUES (4,4,2,2,'2019-01-04',NULL);
INSERT INTO lotacao VALUES (5,5,2,2,'2019-01-05',NULL);
INSERT INTO lotacao VALUES (6,6,2,2,'2019-01-06',NULL);
INSERT INTO lotacao VALUES (7,7,2,2,'2019-01-07',NULL);
INSERT INTO lotacao VALUES (8,8,2,7,'2019-01-08','2019-12-30');
INSERT INTO lotacao VALUES (9,9,2,2,'2019-01-09',NULL);
INSERT INTO lotacao VALUES (10,10,1,2,'2019-01-19',NULL);

INSERT INTO livro VALUES (1,2,1,2019,1,0);
INSERT INTO livro VALUES (2,2,3,2019,1,0);
INSERT INTO livro VALUES (3,2,2,2019,1,1);
INSERT INTO livro VALUES (4,2,2,2019,2,1);
INSERT INTO livro VALUES (5,2,2,2019,3,1);
INSERT INTO livro VALUES (6,2,2,2019,4,1);
INSERT INTO livro VALUES (7,2,2,2019,5,1);
INSERT INTO livro VALUES (8,2,2,2019,6,1);
INSERT INTO livro VALUES (9,2,2,2019,7,1);
INSERT INTO livro VALUES (10,2,2,2019,8,0);

INSERT INTO pagina VALUES (1,1,1);
INSERT INTO pagina VALUES (2,2,1);
INSERT INTO pagina VALUES (3,3,1);
INSERT INTO pagina VALUES (4,3,2);
INSERT INTO pagina VALUES (5,3,3);
INSERT INTO pagina VALUES (6,3,4);
INSERT INTO pagina VALUES (7,3,5);
INSERT INTO pagina VALUES (8,3,6);
INSERT INTO pagina VALUES (9,3,7);
INSERT INTO pagina VALUES (10,3,8);

INSERT INTO protocolo VALUES (1,1,2,1,3,1,'2019-10-20');
INSERT INTO protocolo VALUES (2,2,2,2,3,1,'2019-10-21');
INSERT INTO protocolo VALUES (3,3,2,3,3,1,'2019-10-22');
INSERT INTO protocolo VALUES (4,4,2,4,3,1,'2019-10-23');
INSERT INTO protocolo VALUES (5,5,2,5,3,1,'2019-10-24');
INSERT INTO protocolo VALUES (6,6,2,6,4,1,'2019-10-25');
INSERT INTO protocolo VALUES (7,7,2,7,4,1,'2019-10-26');
INSERT INTO protocolo VALUES (8,8,2,8,4,1,'2019-10-27');
INSERT INTO protocolo VALUES (9,9,2,9,4,1,'2019-10-28');
INSERT INTO protocolo VALUES (10,10,2,10,4,0,'2019-10-29');