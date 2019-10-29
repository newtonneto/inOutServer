-- MySQL dump 10.13  Distrib 8.0.17, for Win64 (x86_64)
--
-- Host: localhost    Database: inout
-- ------------------------------------------------------
-- Server version	8.0.17

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `documento`
--

DROP TABLE IF EXISTS `documento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8 */;
CREATE TABLE `documento` (
  `id` int(11) NOT NULL,
  `fk_user` int(11) NOT NULL,
  `fk_processo` int(11) DEFAULT NULL,
  `data_de_recebimento` date NOT NULL,
  `tipo` int(11) NOT NULL DEFAULT '10',
  `numero` varchar(30) NOT NULL,
  `emissor` varchar(50) NOT NULL,
  `assunto` varchar(1000) NOT NULL,
  `despacho` varchar(200) NOT NULL,
  `entrega_pessoal` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `fk_user` (`fk_user`),
  KEY `fk_processo` (`fk_processo`),
  CONSTRAINT `documento_ibfk_1` FOREIGN KEY (`fk_user`) REFERENCES `user` (`id`),
  CONSTRAINT `documento_ibfk_2` FOREIGN KEY (`fk_processo`) REFERENCES `processo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `documento`
--

LOCK TABLES `documento` WRITE;
/*!40000 ALTER TABLE `documento` DISABLE KEYS */;
INSERT INTO `documento` VALUES (1,1,1,'2019-10-01',10,'001/2019','SEMURB','Expediente Extraordinario','SGFU',0),(2,1,2,'2019-10-02',10,'002/2019','SEMPLA','Protocolo Digital','DCRA',0),(3,1,3,'2019-10-03',10,'003/2019','IDEMA','Denuncia','SGFA',0),(4,1,4,'2019-10-04',1,'004/2019','IPHAN','Reforma do Palacio Felipe Camarão','SAIPUA',0),(5,2,5,'2019-10-05',2,'005/2019','MPF','Denuncia','SGFA',0),(6,2,6,'2019-10-06',3,'006/2019','PGM','Solicitação de informações','DGSIG',1),(7,3,7,'2019-10-07',4,'007/2019','CMG','Prestação de contas','DAG',1),(8,3,8,'2019-10-08',5,'008/2019','SEMAD','Contratos de estagio','RH',1),(9,4,9,'2019-10-09',6,'009/2019','UFRN','Solicitação de informações','DGSIG',1),(10,4,10,'2019-10-10',7,'010/2019','IFRN','Denuncia','SGFA',1),(11,1,NULL,'2019-10-10',11,'011/2019','NUPACIV','Certidão Fundiaria','DGSIG',0);
/*!40000 ALTER TABLE `documento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `livro`
--

DROP TABLE IF EXISTS `livro`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8 */;
CREATE TABLE `livro` (
  `id` int(11) NOT NULL,
  `fk_setor` int(11) NOT NULL,
  `tipo` int(11) NOT NULL DEFAULT '2',
  `ano` int(11) NOT NULL,
  `volume` int(11) NOT NULL DEFAULT '1',
  `encerrado` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `fk_setor` (`fk_setor`),
  CONSTRAINT `livro_ibfk_1` FOREIGN KEY (`fk_setor`) REFERENCES `setor` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `livro`
--

LOCK TABLES `livro` WRITE;
/*!40000 ALTER TABLE `livro` DISABLE KEYS */;
INSERT INTO `livro` VALUES (1,2,1,2019,1,0),(2,2,3,2019,1,0),(3,2,2,2019,1,1),(4,2,2,2019,2,1),(5,2,2,2019,3,1),(6,2,2,2019,4,1),(7,2,2,2019,5,1),(8,2,2,2019,6,1),(9,2,2,2019,7,1),(10,2,2,2019,8,0);
/*!40000 ALTER TABLE `livro` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orgao`
--

DROP TABLE IF EXISTS `orgao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8 */;
CREATE TABLE `orgao` (
  `id` int(11) NOT NULL,
  `nome` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orgao`
--

LOCK TABLES `orgao` WRITE;
/*!40000 ALTER TABLE `orgao` DISABLE KEYS */;
INSERT INTO `orgao` VALUES (1,'SEMURB'),(2,'SEMPLA'),(3,'SEMTAS'),(4,'SMS'),(5,'SMG'),(6,'CGM'),(7,'PGM'),(8,'SEMDES'),(9,'SEMOV'),(10,'SEMUT');
/*!40000 ALTER TABLE `orgao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pagina`
--

DROP TABLE IF EXISTS `pagina`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8 */;
CREATE TABLE `pagina` (
  `id` int(11) NOT NULL,
  `fk_livro` int(11) NOT NULL,
  `numero` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_livro` (`fk_livro`),
  CONSTRAINT `pagina_ibfk_1` FOREIGN KEY (`fk_livro`) REFERENCES `livro` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pagina`
--

LOCK TABLES `pagina` WRITE;
/*!40000 ALTER TABLE `pagina` DISABLE KEYS */;
INSERT INTO `pagina` VALUES (1,1,1),(2,2,1),(3,3,1),(4,3,2),(5,3,3),(6,3,4),(7,3,5),(8,3,6),(9,3,7),(10,3,8);
/*!40000 ALTER TABLE `pagina` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prazo`
--

DROP TABLE IF EXISTS `prazo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8 */;
CREATE TABLE `prazo` (
  `id` int(11) NOT NULL,
  `fk_documento` int(11) NOT NULL,
  `tipo` int(11) NOT NULL,
  `vencimento` datetime NOT NULL,
  `encerrado` tinyint(4) NOT NULL DEFAULT '0',
  `dilacao` tinyint(4) NOT NULL DEFAULT '0',
  `quantidade_de_dilacoes` int(11) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `fk_documento` (`fk_documento`),
  CONSTRAINT `prazo_ibfk_1` FOREIGN KEY (`fk_documento`) REFERENCES `documento` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prazo`
--

LOCK TABLES `prazo` WRITE;
/*!40000 ALTER TABLE `prazo` DISABLE KEYS */;
INSERT INTO `prazo` VALUES (1,1,1,'2019-11-01 00:00:00',0,0,0),(2,1,2,'2019-11-02 00:00:00',1,1,4),(3,1,3,'2019-11-03 00:00:00',0,0,0),(4,2,4,'2019-11-04 00:00:00',1,0,0),(5,2,5,'2019-11-05 00:00:00',0,0,0),(6,2,6,'2019-11-06 00:00:00',1,0,0),(7,3,1,'2019-11-07 00:00:00',0,1,2),(8,3,2,'2019-11-08 00:00:00',1,0,0),(9,3,3,'2019-11-09 00:00:00',0,0,0),(10,4,4,'2019-11-10 00:00:00',1,1,1);
/*!40000 ALTER TABLE `prazo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `processo`
--

DROP TABLE IF EXISTS `processo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8 */;
CREATE TABLE `processo` (
  `id` int(11) NOT NULL,
  `numero` varchar(21) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `processo`
--

LOCK TABLES `processo` WRITE;
/*!40000 ALTER TABLE `processo` DISABLE KEYS */;
INSERT INTO `processo` VALUES (1,'123456/2019-01'),(2,'123456/2019-02'),(3,'123456/2019-03'),(4,'123456/2019-04'),(5,'123456/2019-05'),(6,'123456/2019-06'),(7,'123456/2019-07'),(8,'123456/2019-08'),(9,'123456/2019-09'),(10,'123456/2019-10');
/*!40000 ALTER TABLE `processo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `protocolo`
--

DROP TABLE IF EXISTS `protocolo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8 */;
CREATE TABLE `protocolo` (
  `id` int(11) NOT NULL,
  `fk_documento` int(11) NOT NULL,
  `fk_setor_origem` int(11) NOT NULL,
  `fk_setor_destino` int(11) NOT NULL,
  `fk_pagina` int(11) NOT NULL,
  `entregue` tinyint(4) NOT NULL,
  `data_da_entrega` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_documento` (`fk_documento`),
  KEY `fk_setor_origem` (`fk_setor_origem`),
  KEY `fk_setor_destino` (`fk_setor_destino`),
  KEY `fk_pagina` (`fk_pagina`),
  CONSTRAINT `protocolo_ibfk_1` FOREIGN KEY (`fk_documento`) REFERENCES `documento` (`id`),
  CONSTRAINT `protocolo_ibfk_2` FOREIGN KEY (`fk_setor_origem`) REFERENCES `setor` (`id`),
  CONSTRAINT `protocolo_ibfk_3` FOREIGN KEY (`fk_setor_destino`) REFERENCES `setor` (`id`),
  CONSTRAINT `protocolo_ibfk_4` FOREIGN KEY (`fk_pagina`) REFERENCES `pagina` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `protocolo`
--

LOCK TABLES `protocolo` WRITE;
/*!40000 ALTER TABLE `protocolo` DISABLE KEYS */;
INSERT INTO `protocolo` VALUES (1,1,2,1,3,1,'2019-10-20'),(2,2,2,2,3,1,'2019-10-21'),(3,3,2,3,3,1,'2019-10-22'),(4,4,2,4,3,1,'2019-10-23'),(5,5,2,5,3,1,'2019-10-24'),(6,6,2,6,4,1,'2019-10-25'),(7,7,2,7,4,1,'2019-10-26'),(8,8,2,8,4,1,'2019-10-27'),(9,9,2,9,4,1,'2019-10-28'),(10,10,2,10,4,0,'2019-10-29');
/*!40000 ALTER TABLE `protocolo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `setor`
--

DROP TABLE IF EXISTS `setor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8 */;
CREATE TABLE `setor` (
  `id` int(11) NOT NULL,
  `fk_orgao` int(11) NOT NULL,
  `nome` int(11) NOT NULL,
  `ativo` tinyint(4) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `fk_orgao` (`fk_orgao`),
  CONSTRAINT `setor_ibfk_1` FOREIGN KEY (`fk_orgao`) REFERENCES `orgao` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `setor`
--

LOCK TABLES `setor` WRITE;
/*!40000 ALTER TABLE `setor` DISABLE KEYS */;
INSERT INTO `setor` VALUES (1,1,1,1),(2,1,2,1),(3,1,3,1),(4,1,4,1),(5,1,5,1),(6,1,6,1),(7,1,7,1),(8,1,8,1),(9,1,9,1),(10,1,10,0);
/*!40000 ALTER TABLE `setor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(32) NOT NULL,
  `first_name` varchar(15) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `grupo` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'newton','123','newton','neto','newton@email.com',NULL),(2,'joseane','321','joseane','lima','josy@email.com',NULL),(3,'juliana','213','juliana','medeiros','juh@email.com',NULL),(4,'lenise','312','lenise','naosei','lili@email.com',NULL),(5,'nadja','1234','nadja','rafaela','nadja@email.com',NULL),(6,'thiago','4321','thiago','naosei','thiago@email.com',NULL),(7,'daniel','1243','daniel','nicolau','daniel@email.com',NULL),(8,'alessandra','4312','alessandra','condera','alessandra@email.com',NULL),(9,'ana','1324','ana','carolina','ana@email.com',NULL),(10,'izolda','4231','izolda','naosei','izolda@email.com',NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-10-28 22:21:40
