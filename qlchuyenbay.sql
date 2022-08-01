-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: localhost    Database: qlchuyenbay
-- ------------------------------------------------------
-- Server version	8.0.28

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
-- Table structure for table `chi_tiet_hoa_don`
--

DROP TABLE IF EXISTS `chi_tiet_hoa_don`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chi_tiet_hoa_don` (
  `ma_hoa_don` int NOT NULL,
  `ma_ve` int NOT NULL,
  `so_luong` int DEFAULT NULL,
  `thanh_tien` float DEFAULT NULL,
  PRIMARY KEY (`ma_hoa_don`,`ma_ve`),
  KEY `ma_ve` (`ma_ve`),
  CONSTRAINT `chi_tiet_hoa_don_ibfk_1` FOREIGN KEY (`ma_hoa_don`) REFERENCES `hoa_don` (`id`),
  CONSTRAINT `chi_tiet_hoa_don_ibfk_2` FOREIGN KEY (`ma_ve`) REFERENCES `ve` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chi_tiet_hoa_don`
--

LOCK TABLES `chi_tiet_hoa_don` WRITE;
/*!40000 ALTER TABLE `chi_tiet_hoa_don` DISABLE KEYS */;
INSERT INTO `chi_tiet_hoa_don` VALUES (1,1,2,1),(1,2,1,5);
/*!40000 ALTER TABLE `chi_tiet_hoa_don` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chuyen_bay`
--

DROP TABLE IF EXISTS `chuyen_bay`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chuyen_bay` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ngay_gio` datetime NOT NULL,
  `thoi_gian_bay` time NOT NULL,
  `sl_ghe_hang1` int NOT NULL,
  `sl_ghe_hang2` int NOT NULL,
  `san_bay_trung_gian` int DEFAULT NULL,
  `thoi_gian_dung` time DEFAULT NULL,
  `ghi_chu` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ma_tuyen_bay` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `san_bay_trung_gian` (`san_bay_trung_gian`),
  KEY `ma_tuyen_bay` (`ma_tuyen_bay`),
  CONSTRAINT `chuyen_bay_ibfk_1` FOREIGN KEY (`san_bay_trung_gian`) REFERENCES `san_bay` (`id`),
  CONSTRAINT `chuyen_bay_ibfk_2` FOREIGN KEY (`ma_tuyen_bay`) REFERENCES `tuyen_bay` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chuyen_bay`
--

LOCK TABLES `chuyen_bay` WRITE;
/*!40000 ALTER TABLE `chuyen_bay` DISABLE KEYS */;
INSERT INTO `chuyen_bay` VALUES (1,'VN01','2022-01-29 16:36:00','02:00:00',3,5,3,'00:25:00','Do xang',1),(2,'VN02','2022-01-29 16:37:00','02:00:00',3,5,NULL,NULL,NULL,1);
/*!40000 ALTER TABLE `chuyen_bay` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hang_ve`
--

DROP TABLE IF EXISTS `hang_ve`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hang_ve` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ten` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `gia` float NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hang_ve`
--

LOCK TABLES `hang_ve` WRITE;
/*!40000 ALTER TABLE `hang_ve` DISABLE KEYS */;
INSERT INTO `hang_ve` VALUES (1,'Eco',1),(2,'Bsu',5);
/*!40000 ALTER TABLE `hang_ve` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hoa_don`
--

DROP TABLE IF EXISTS `hoa_don`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hoa_don` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ngay_tao` datetime DEFAULT NULL,
  `ma_user` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ma_user` (`ma_user`),
  CONSTRAINT `hoa_don_ibfk_1` FOREIGN KEY (`ma_user`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hoa_don`
--

LOCK TABLES `hoa_don` WRITE;
/*!40000 ALTER TABLE `hoa_don` DISABLE KEYS */;
INSERT INTO `hoa_don` VALUES (1,'2022-01-17 16:33:47',2);
/*!40000 ALTER TABLE `hoa_don` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rule`
--

DROP TABLE IF EXISTS `rule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rule` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sl_sanbay` int NOT NULL,
  `sl_hang_ve` int NOT NULL,
  `san_bay_trung_gian_max` int NOT NULL,
  `time_bay_min` time NOT NULL,
  `time_dung_min` time NOT NULL,
  `time_dung_max` time NOT NULL,
  `time_ban_ve` time NOT NULL,
  `time_dat_ve` time NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rule`
--

LOCK TABLES `rule` WRITE;
/*!40000 ALTER TABLE `rule` DISABLE KEYS */;
/*!40000 ALTER TABLE `rule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `san_bay`
--

DROP TABLE IF EXISTS `san_bay`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `san_bay` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ma_san_bay` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ten_thanh_pho` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ma_san_bay` (`ma_san_bay`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `san_bay`
--

LOCK TABLES `san_bay` WRITE;
/*!40000 ALTER TABLE `san_bay` DISABLE KEYS */;
INSERT INTO `san_bay` VALUES (1,'HAN','Hà Nội'),(2,'HPH','Hải Phòng'),(3,'DIN','Điện Biên Phủ'),(4,'THD','Thanh Hóa'),(5,'VII','Vinh'),(6,'VDH','Đồng Hới'),(7,'HUI','Huế'),(8,'DAD','Đà Nẵng'),(9,'VCL','Quảng Nam'),(10,'UIH','Qui Nhơn');
/*!40000 ALTER TABLE `san_bay` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tuyen_bay`
--

DROP TABLE IF EXISTS `tuyen_bay`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tuyen_bay` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ma_san_bay_di` int NOT NULL,
  `ma_san_bay_den` int NOT NULL,
  `active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ma_san_bay_di` (`ma_san_bay_di`),
  KEY `ma_san_bay_den` (`ma_san_bay_den`),
  CONSTRAINT `tuyen_bay_ibfk_1` FOREIGN KEY (`ma_san_bay_di`) REFERENCES `san_bay` (`id`),
  CONSTRAINT `tuyen_bay_ibfk_2` FOREIGN KEY (`ma_san_bay_den`) REFERENCES `san_bay` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tuyen_bay`
--

LOCK TABLES `tuyen_bay` WRITE;
/*!40000 ALTER TABLE `tuyen_bay` DISABLE KEYS */;
INSERT INTO `tuyen_bay` VALUES (1,'Hà Nội - Hải Phòng',1,2,1);
/*!40000 ALTER TABLE `tuyen_bay` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `joined_date` datetime DEFAULT NULL,
  `avatar` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_role` enum('ADMIN','EMPLOYEE','USER') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','admin','c4ca4238a0b923820dcc509a6f75849b','admin@gmail.com',1,'2022-01-17 16:33:47','images/defaultava.jpg','ADMIN'),(2,'test','test','c4ca4238a0b923820dcc509a6f75849b','test@gmail.com',1,'2022-01-17 16:33:47','images/defaultava.jpg','USER');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ve`
--

DROP TABLE IF EXISTS `ve`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ve` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ma_chuyen_bay` int NOT NULL,
  `ma_hang_ve` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ma_chuyen_bay` (`ma_chuyen_bay`),
  KEY `ma_hang_ve` (`ma_hang_ve`),
  CONSTRAINT `ve_ibfk_1` FOREIGN KEY (`ma_chuyen_bay`) REFERENCES `chuyen_bay` (`id`),
  CONSTRAINT `ve_ibfk_2` FOREIGN KEY (`ma_hang_ve`) REFERENCES `hang_ve` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ve`
--

LOCK TABLES `ve` WRITE;
/*!40000 ALTER TABLE `ve` DISABLE KEYS */;
INSERT INTO `ve` VALUES (1,1,1),(2,1,2),(3,2,1),(4,2,2);
/*!40000 ALTER TABLE `ve` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-08-01 12:11:40
