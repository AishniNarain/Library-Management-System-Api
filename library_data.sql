USE dbname;

-- MySQL dump 10.13  Distrib 8.0.37, for Linux (x86_64)
--
-- Host: localhost    Database: library_api
-- ------------------------------------------------------
-- Server version	8.0.37

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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('da214aa38534');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `block_list`
--

DROP TABLE IF EXISTS `block_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `block_list` (
  `id` int NOT NULL AUTO_INCREMENT,
  `jti` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `block_list`
--

LOCK TABLES `block_list` WRITE;
/*!40000 ALTER TABLE `block_list` DISABLE KEYS */;
INSERT INTO `block_list` VALUES (1,'b45cfaf1-30dc-41a2-ba25-09463c94321e','2024-05-21 00:00:00');
/*!40000 ALTER TABLE `block_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `books` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(50) DEFAULT NULL,
  `author` varchar(50) NOT NULL,
  `publisher` varchar(50) NOT NULL,
  `total_copies` int DEFAULT NULL,
  `available_copies` int DEFAULT NULL,
  `added_on` date DEFAULT NULL,
  `updated_on` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books`
--

LOCK TABLES `books` WRITE;
/*!40000 ALTER TABLE `books` DISABLE KEYS */;
INSERT INTO `books` VALUES (1,'Gulliver\'s Travels','Jonathan Swift','Knopf : Distributed by Random House',10,9,'2024-05-21',NULL),(2,'The Adventures of Huckleberry Finn','Mark Twain','Norton, New York',8,8,'2024-05-21',NULL),(3,'The Adventures of Tom Sawyer','Mark Twain','Sterling, New York',10,10,'2024-05-21',NULL),(4,'Pride and Prejudice','Jane Austen','Modern Library, New York',10,9,'2024-05-21',NULL),(5,'A Christmas Carol','Charles Dickens','HarperCollins Children\'s Books, New York',8,7,'2024-05-21',NULL),(6,'Oliver Twist','Charles Dickens','Knopf : Distributed by Random House, New York',8,6,'2024-05-21',NULL),(20,'Oliver Twist','Charles Dickens','Knopf : Distributed by Random House, New York',8,8,'2024-05-21',NULL),(21,'Oliver Twist','Charles Dickens','Knopf : Distributed by Random House, New York',8,8,'2024-05-21',NULL);
/*!40000 ALTER TABLE `books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `borrow_books`
--

DROP TABLE IF EXISTS `borrow_books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `borrow_books` (
  `id` int NOT NULL AUTO_INCREMENT,
  `issue_date` date DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `issued_by` int DEFAULT NULL,
  `fine` int DEFAULT NULL,
  `fine_days` int DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  `expected_return_date` date DEFAULT NULL,
  `return_date` date DEFAULT NULL,
  `student_id` int DEFAULT NULL,
  `books_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `books_id` (`books_id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `borrow_books_ibfk_1` FOREIGN KEY (`books_id`) REFERENCES `books` (`id`),
  CONSTRAINT `borrow_books_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `borrow_books`
--

LOCK TABLES `borrow_books` WRITE;
/*!40000 ALTER TABLE `borrow_books` DISABLE KEYS */;
INSERT INTO `borrow_books` VALUES (1,'2024-05-21','2024-05-22',5,0,0,'No fine',NULL,NULL,3,1),(2,'2024-05-21','2024-05-22',5,0,0,'Returned','2024-05-21','2024-05-21',3,3),(3,'2024-05-21','2024-05-22',5,0,0,'No fine',NULL,NULL,3,6),(4,'2024-05-21','2024-05-22',5,0,0,'No fine',NULL,NULL,4,6),(5,'2024-04-21','2024-05-22',5,0,0,'No fine',NULL,NULL,4,5),(6,'2024-04-21','2024-04-22',5,0,0,'Returned',NULL,'2024-05-21',6,2),(7,'2024-04-20','2024-08-20',5,0,0,'No fine',NULL,NULL,6,4);
/*!40000 ALTER TABLE `borrow_books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permissions`
--

DROP TABLE IF EXISTS `permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `permission_name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `permission_name` (`permission_name`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permissions`
--

LOCK TABLES `permissions` WRITE;
/*!40000 ALTER TABLE `permissions` DISABLE KEYS */;
INSERT INTO `permissions` VALUES (5,'Block Users'),(8,'Create Inventory'),(10,'Delete Inventory'),(4,'Delete Users'),(11,'Issue Books'),(1,'Register Users'),(13,'Return Books'),(15,'Send Emails'),(6,'Unblock Users'),(9,'Update Inventory'),(3,'Update Users'),(7,'View Inventory'),(12,'View Issued Books'),(14,'View Issued Books History'),(2,'View Users');
/*!40000 ALTER TABLE `permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `role_name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `role_name` (`role_name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'Admin'),(4,'Guest User'),(2,'Librarian'),(3,'Student');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_roles_and_permissions`
--

DROP TABLE IF EXISTS `user_roles_and_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_roles_and_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `role_id` int DEFAULT NULL,
  `permission_ids` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `role_id` (`role_id`),
  KEY `ix_user_roles_and_permissions_user_id` (`user_id`),
  CONSTRAINT `user_roles_and_permissions_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`),
  CONSTRAINT `user_roles_and_permissions_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_roles_and_permissions`
--

LOCK TABLES `user_roles_and_permissions` WRITE;
/*!40000 ALTER TABLE `user_roles_and_permissions` DISABLE KEYS */;
INSERT INTO `user_roles_and_permissions` VALUES (1,1,1,'1,2,3,4,5,6,7,8,10'),(2,2,4,'7'),(3,5,2,'1,2,4,5,6,7,9,11,13,12,14,15'),(4,7,2,'1,2,4,5,6,7,9,11,13,12,14,15'),(5,3,3,'7,12,14'),(6,4,3,'7,12,14'),(7,6,3,'7,12,14');
/*!40000 ALTER TABLE `user_roles_and_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(50) NOT NULL,
  `registration_date` datetime DEFAULT NULL,
  `login_date` datetime DEFAULT NULL,
  `block_status` tinyint(1) DEFAULT NULL,
  `created_by` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_email` (`email`),
  UNIQUE KEY `ix_users_username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Aishni','aishni@gmail.com','Aish123','2024-05-21 00:00:00','2024-05-28 00:00:00',NULL,NULL),(2,'Sankalp','san@gmail.com','San12345','2024-05-21 00:00:00',NULL,0,1),(3,'Alka','alka@gmail.com','Alka12345','2024-05-21 00:00:00',NULL,0,1),(4,'Sakshi','sak@gmail.com','Sak12345','2024-05-21 00:00:00',NULL,0,1),(5,'Aman','aman@gmail.com','Aman12345','2024-05-21 00:00:00','2024-05-22 00:00:00',0,1),(6,'Rohan','roh@gmail.com','Roh12345','2024-05-21 00:00:00',NULL,0,1),(7,'Abhishek','abhi@gmail.com','Abhi12345','2024-05-21 00:00:00',NULL,0,1),(8,'Aishwarya','aish@gmail.com','Aish12345','2024-05-21 00:00:00',NULL,0,1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-03 17:01:06
