/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.11.14-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: tabcore_db
-- ------------------------------------------------------
-- Server version	10.11.14-MariaDB-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bulk_inventory`
--

DROP TABLE IF EXISTS `bulk_inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `bulk_inventory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `district` varchar(50) NOT NULL,
  `item_name` varchar(100) NOT NULL,
  `good_qty` int(11) DEFAULT 0,
  `defective_qty` int(11) DEFAULT 0,
  `remark` text DEFAULT NULL,
  `last_updated` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_item_district` (`district`,`item_name`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bulk_inventory`
--

LOCK TABLES `bulk_inventory` WRITE;
/*!40000 ALTER TABLE `bulk_inventory` DISABLE KEYS */;
INSERT INTO `bulk_inventory` VALUES
(1,'Anuradhapura','Stylus Pen',0,0,'','2026-03-24 08:28:05'),
(2,'Anuradhapura','Rugged Pouch',0,0,'','2026-03-24 08:27:53'),
(3,'Anuradhapura','Delivery Bag',0,0,'','2026-03-24 08:27:43'),
(4,'Badulla','Stylus Pen',0,0,'','2026-03-24 08:05:57'),
(5,'Badulla','Rugged Pouch',0,0,'','2026-03-24 08:05:40'),
(6,'Badulla','Delivery Bag',0,0,'','2026-03-24 08:05:22'),
(7,'Batticaloa','Stylus Pen',0,0,'','2026-03-24 08:06:16'),
(8,'Batticaloa','Rugged Pouch',0,0,'','2026-03-24 05:52:48'),
(9,'Batticaloa','Delivery Bag',0,0,'','2026-03-24 05:52:48'),
(10,'Colombo','Stylus Pen',0,0,'','2026-03-24 08:06:58'),
(11,'Colombo','Rugged Pouch',0,0,'','2026-03-24 08:06:48'),
(12,'Colombo','Delivery Bag',0,0,'','2026-03-24 08:06:36'),
(13,'Gampaha','Stylus Pen',0,0,'','2026-03-24 05:52:48'),
(14,'Gampaha','Rugged Pouch',0,0,'','2026-03-24 05:52:48'),
(15,'Gampaha','Delivery Bag',0,0,'','2026-03-24 05:52:48'),
(16,'Kegalle','Stylus Pen',0,0,'','2026-03-24 05:52:48'),
(17,'Kegalle','Rugged Pouch',0,0,'','2026-03-24 05:52:48'),
(18,'Kegalle','Delivery Bag',0,0,'','2026-03-24 05:52:48'),
(19,'Polonnaruwa','Stylus Pen',0,0,'','2026-03-24 05:52:48'),
(20,'Polonnaruwa','Rugged Pouch',0,0,'','2026-03-24 05:52:48'),
(21,'Polonnaruwa','Delivery Bag',0,0,'','2026-03-24 08:07:11'),
(22,'Ratnapura','Stylus Pen',0,0,'','2026-03-24 08:07:50'),
(23,'Ratnapura','Rugged Pouch',0,0,'','2026-03-24 08:08:25'),
(24,'Ratnapura','Delivery Bag',0,0,'','2026-03-24 08:07:29'),
(25,'Trincomalee','Stylus Pen',0,0,'','2026-03-24 05:52:48'),
(26,'Trincomalee','Rugged Pouch',0,0,'','2026-03-24 05:52:48'),
(27,'Trincomalee','Delivery Bag',0,0,'','2026-03-24 05:52:48');
/*!40000 ALTER TABLE `bulk_inventory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device_history`
--

DROP TABLE IF EXISTS `device_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `device_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tablet_id` int(11) NOT NULL,
  `action` varchar(50) NOT NULL,
  `performed_by` varchar(100) NOT NULL,
  `status_changed_to` varchar(50) DEFAULT NULL,
  `notes` text DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `tablet_id` (`tablet_id`),
  CONSTRAINT `device_history_ibfk_1` FOREIGN KEY (`tablet_id`) REFERENCES `tablets` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device_history`
--

LOCK TABLES `device_history` WRITE;
/*!40000 ALTER TABLE `device_history` DISABLE KEYS */;
INSERT INTO `device_history` VALUES
(1,1,'Registered','Sarinda','Pending','Manual Registration','2026-03-24 09:46:50'),
(2,1,'Locked for Inspection','Sarinda','Locked','Technician opened for inspection','2026-03-24 09:46:59'),
(3,1,'Inspected','Sarinda','Passed','Verdict: Passed','2026-03-24 09:47:06'),
(4,1,'Inspection Undone','Sarinda','Pending','User reversed the inspection decision. Moved back to Queue.','2026-03-24 09:47:44'),
(5,1,'Locked for Inspection','Sarinda','Locked','Technician opened for inspection','2026-03-24 09:47:46'),
(6,1,'Inspected','Sarinda','Passed','Verdict: Passed','2026-03-24 09:47:51'),
(7,1,'Data Edited','Sarinda','Passed','Admin updated device details and inspection data.','2026-03-24 09:48:08');
/*!40000 ALTER TABLE `device_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `district_targets`
--

DROP TABLE IF EXISTS `district_targets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `district_targets` (
  `district_name` varchar(100) NOT NULL,
  `target_count` int(11) DEFAULT 0,
  PRIMARY KEY (`district_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `district_targets`
--

LOCK TABLES `district_targets` WRITE;
/*!40000 ALTER TABLE `district_targets` DISABLE KEYS */;
INSERT INTO `district_targets` VALUES
('Anuradhapura',7),
('Badulla',81),
('Batticaloa',54),
('Colombo',108),
('Gampaha',77),
('Kegalle',58),
('Polonnaruwa',12),
('Ratnapura',106),
('Trincomalee',40);
/*!40000 ALTER TABLE `district_targets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inspections`
--

DROP TABLE IF EXISTS `inspections`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `inspections` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tablet_id` int(11) DEFAULT NULL,
  `inspected_by` varchar(50) DEFAULT NULL,
  `physical_condition` varchar(20) DEFAULT NULL,
  `display_status` varchar(20) DEFAULT NULL,
  `touch_response` varchar(20) DEFAULT NULL,
  `battery_health` varchar(20) DEFAULT NULL,
  `wifi_bt_status` varchar(20) DEFAULT NULL,
  `camera_status` varchar(20) DEFAULT NULL,
  `speaker_mic_status` varchar(20) DEFAULT NULL,
  `port_condition` varchar(20) DEFAULT NULL,
  `verdict` varchar(20) DEFAULT NULL,
  `comments` text DEFAULT NULL,
  `inspection_date` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `tablet_id` (`tablet_id`),
  CONSTRAINT `inspections_ibfk_1` FOREIGN KEY (`tablet_id`) REFERENCES `tablets` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inspections`
--

LOCK TABLES `inspections` WRITE;
/*!40000 ALTER TABLE `inspections` DISABLE KEYS */;
/*!40000 ALTER TABLE `inspections` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory_logs`
--

DROP TABLE IF EXISTS `inventory_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory_logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `district` varchar(50) DEFAULT NULL,
  `item_name` varchar(100) DEFAULT NULL,
  `good_qty_changed` int(11) DEFAULT NULL,
  `defective_qty_changed` int(11) DEFAULT NULL,
  `remark` text DEFAULT NULL,
  `action_time` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_logs`
--

LOCK TABLES `inventory_logs` WRITE;
/*!40000 ALTER TABLE `inventory_logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `inventory_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `settings`
--

DROP TABLE IF EXISTS `settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `settings` (
  `id` int(11) NOT NULL,
  `batch_target` int(11) DEFAULT 540,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `settings`
--

LOCK TABLES `settings` WRITE;
/*!40000 ALTER TABLE `settings` DISABLE KEYS */;
INSERT INTO `settings` VALUES
(1,540);
/*!40000 ALTER TABLE `settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_audit`
--

DROP TABLE IF EXISTS `system_audit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_audit` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action` varchar(100) NOT NULL,
  `performed_by` varchar(100) NOT NULL,
  `details` text DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=702 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_audit`
--

LOCK TABLES `system_audit` WRITE;
/*!40000 ALTER TABLE `system_audit` DISABLE KEYS */;
INSERT INTO `system_audit` VALUES
(1,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-12 10:32:20'),
(2,'User Login','Dhammika','User \'dhammika\' logged in successfully.','2026-03-12 10:32:23'),
(3,'User Logout','Dhammika','User \'dhammika\' logged out.','2026-03-12 10:32:27'),
(4,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-12 10:32:31'),
(5,'Settings Updated','Sarinda','Batch target updated to 540.','2026-03-12 10:46:49'),
(6,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-13 03:21:40'),
(7,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-13 03:21:44'),
(8,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-13 03:22:27'),
(9,'User Login','Laksaman','User \'laksaman\' logged in successfully.','2026-03-13 04:47:21'),
(10,'Device Force Unlocked','Sarinda','Admin unlocked tablet T-43.','2026-03-13 04:52:05'),
(11,'User Created','Sarinda','Created new user \'pubudu\' with role \'Technician\'.','2026-03-13 04:54:34'),
(12,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-13 07:05:06'),
(13,'Device Force Unlocked','Sarinda','Admin unlocked tablet T-43.','2026-03-13 07:17:56'),
(14,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-13 07:18:19'),
(15,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-13 07:24:04'),
(16,'Device Deleted','Sarinda','Admin deleted tablet T-9 from the system permanently.','2026-03-13 08:01:14'),
(17,'Device Deleted','Sarinda','Admin deleted tablet T-54 from the system permanently.','2026-03-13 08:01:48'),
(18,'Device Deleted','Sarinda','Admin deleted tablet T-55 from the system permanently.','2026-03-13 08:01:55'),
(19,'Device Deleted','Sarinda','Admin deleted tablet T-56 from the system permanently.','2026-03-13 08:02:06'),
(20,'Device Deleted','Sarinda','Admin deleted tablet T-10 from the system permanently.','2026-03-13 08:10:25'),
(21,'Device Deleted','Sarinda','Admin deleted tablet T-7 from the system permanently.','2026-03-13 08:10:36'),
(22,'Device Deleted','Sarinda','Admin deleted tablet T-51 from the system permanently.','2026-03-13 08:19:56'),
(23,'Device Edited','Sarinda','Admin updated data for tablet T-50.','2026-03-13 08:28:24'),
(24,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-13 08:35:26'),
(25,'Device Deleted','Sarinda','Admin deleted tablet T-50 from the system permanently.','2026-03-13 08:49:32'),
(26,'Device Force Unlocked','Sarinda','Admin unlocked tablet T-57.','2026-03-13 08:49:42'),
(27,'Device Edited','Sarinda','Admin updated data for tablet T-45.','2026-03-13 08:50:23'),
(28,'Device Edited','Sarinda','Admin updated data for tablet T-45.','2026-03-13 08:50:34'),
(29,'Device Deleted','Sarinda','Admin deleted tablet T-6 from the system permanently.','2026-03-13 10:13:20'),
(30,'Device Deleted','Sarinda','Admin deleted tablet T-16 from the system permanently.','2026-03-13 10:13:29'),
(31,'Device Deleted','Sarinda','Admin deleted tablet T-18 from the system permanently.','2026-03-13 10:20:29'),
(32,'Device Deleted','Sarinda','Admin deleted tablet T-17 from the system permanently.','2026-03-13 10:20:34'),
(33,'Device Deleted','Sarinda','Admin deleted tablet T-15 from the system permanently.','2026-03-13 10:20:38'),
(34,'Device Deleted','Sarinda','Admin deleted tablet T-12 from the system permanently.','2026-03-13 10:20:45'),
(35,'Device Deleted','Sarinda','Admin deleted tablet T-11 from the system permanently.','2026-03-13 10:20:49'),
(36,'Device Edited','Sarinda','Admin updated data for tablet T-59.','2026-03-13 10:21:37'),
(37,'Device Edited','Sarinda','Admin updated data for tablet T-59.','2026-03-13 10:21:50'),
(38,'Device Edited','Sarinda','Admin updated data for tablet T-59.','2026-03-13 10:21:57'),
(39,'Device Edited','Sarinda','Admin updated data for tablet T-59.','2026-03-13 10:22:49'),
(40,'Device Edited','Sarinda','Admin updated data for tablet T-44.','2026-03-13 10:24:35'),
(41,'Device Deleted','Sarinda','Admin deleted tablet T-13 from the system permanently.','2026-03-13 10:57:43'),
(42,'Device Edited','Sarinda','Admin updated data for tablet T-59.','2026-03-13 10:57:54'),
(43,'Device Edited','Sarinda','Admin updated data for tablet T-59.','2026-03-13 10:58:09'),
(44,'Filtered Data Export','Sarinda','Exported filtered report. Filters - District: Colombo, Brand: Lenovo, Status: Passed','2026-03-13 10:58:41'),
(45,'Device Edited','Sarinda','Admin updated data for tablet T-59.','2026-03-13 11:00:44'),
(46,'Filtered Data Export','Sarinda','Exported filtered report. Filters - District: All Districts, Brand: All Brands, Status: All Statuses, Inspector: Susantha','2026-03-13 12:06:09'),
(47,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-13 12:17:18'),
(48,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-13 12:21:27'),
(49,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-13 12:22:28'),
(50,'User Login','Dhammika','User \'dhammika\' logged in successfully.','2026-03-13 12:22:34'),
(51,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-13 12:23:41'),
(52,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-13 12:25:54'),
(53,'User Logout','Dhammika','User \'dhammika\' logged out.','2026-03-13 12:26:24'),
(54,'User Login','Dhammika','User \'dhammika\' logged in successfully.','2026-03-13 12:26:29'),
(55,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-13 12:42:30'),
(56,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-13 15:37:21'),
(57,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-13 17:01:57'),
(58,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-13 17:02:06'),
(59,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-13 17:02:31'),
(60,'User Login','Laksaman','User \'laksaman\' logged in successfully.','2026-03-13 17:02:40'),
(61,'User Logout','Laksaman','User \'laksaman\' logged out.','2026-03-13 17:02:57'),
(62,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-13 17:03:11'),
(63,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-13 17:03:48'),
(64,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-13 17:26:08'),
(65,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-13 17:28:29'),
(66,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-13 17:29:18'),
(67,'Device Force Unlocked','Sarinda','Admin unlocked tablet T-57.','2026-03-13 17:35:28'),
(68,'Filtered Data Export','Sarinda','Exported filtered report. Filters - District: Colombo, Brand: All Brands, Status: All Statuses, Inspector: Sarinda','2026-03-13 17:38:23'),
(69,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-13 17:39:24'),
(70,'Filtered Data Export','Sarinda','Exported filtered report. Filters - District: Colombo, Brand: All Brands, Status: All Statuses, Inspector: All Inspectors','2026-03-13 17:43:17'),
(71,'Settings Updated','Sarinda','Batch target updated to 100.','2026-03-13 17:47:19'),
(72,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-13 17:50:35'),
(73,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-13 17:52:04'),
(74,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-13 18:14:36'),
(75,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-13 18:16:43'),
(76,'Device Deleted','Sarinda','Admin deleted tablet T-59 from the system permanently.','2026-03-13 18:17:17'),
(77,'Device Deleted','Sarinda','Admin deleted tablet T-58 from the system permanently.','2026-03-13 18:17:19'),
(78,'Device Deleted','Sarinda','Admin deleted tablet T-57 from the system permanently.','2026-03-13 18:17:21'),
(79,'Device Deleted','Sarinda','Admin deleted tablet T-45 from the system permanently.','2026-03-13 18:17:24'),
(80,'Device Deleted','Sarinda','Admin deleted tablet T-44 from the system permanently.','2026-03-13 18:17:26'),
(81,'Device Deleted','Sarinda','Admin deleted tablet T-43 from the system permanently.','2026-03-13 18:17:28'),
(82,'Device Deleted','Sarinda','Admin deleted tablet T-42 from the system permanently.','2026-03-13 18:17:30'),
(83,'Device Deleted','Sarinda','Admin deleted tablet T-41 from the system permanently.','2026-03-13 18:17:32'),
(84,'Device Deleted','Sarinda','Admin deleted tablet T-40 from the system permanently.','2026-03-13 18:17:34'),
(85,'Device Deleted','Sarinda','Admin deleted tablet T-39 from the system permanently.','2026-03-13 18:17:35'),
(86,'Device Deleted','Sarinda','Admin deleted tablet T-38 from the system permanently.','2026-03-13 18:17:37'),
(87,'Device Deleted','Sarinda','Admin deleted tablet T-36 from the system permanently.','2026-03-13 18:17:39'),
(88,'Device Deleted','Sarinda','Admin deleted tablet T-34 from the system permanently.','2026-03-13 18:17:41'),
(89,'Device Deleted','Sarinda','Admin deleted tablet T-32 from the system permanently.','2026-03-13 18:17:43'),
(90,'Device Deleted','Sarinda','Admin deleted tablet T-31 from the system permanently.','2026-03-13 18:17:45'),
(91,'Device Deleted','Sarinda','Admin deleted tablet T-30 from the system permanently.','2026-03-13 18:17:47'),
(92,'Device Deleted','Sarinda','Admin deleted tablet T-29 from the system permanently.','2026-03-13 18:17:49'),
(93,'Device Deleted','Sarinda','Admin deleted tablet T-28 from the system permanently.','2026-03-13 18:17:51'),
(94,'Device Deleted','Sarinda','Admin deleted tablet T-27 from the system permanently.','2026-03-13 18:17:53'),
(95,'Device Deleted','Sarinda','Admin deleted tablet T-26 from the system permanently.','2026-03-13 18:17:55'),
(96,'Device Deleted','Sarinda','Admin deleted tablet T-25 from the system permanently.','2026-03-13 18:17:57'),
(97,'Device Deleted','Sarinda','Admin deleted tablet T-24 from the system permanently.','2026-03-13 18:17:59'),
(98,'Device Deleted','Sarinda','Admin deleted tablet T-22 from the system permanently.','2026-03-13 18:18:00'),
(99,'Device Deleted','Sarinda','Admin deleted tablet T-21 from the system permanently.','2026-03-13 18:18:03'),
(100,'Device Deleted','Sarinda','Admin deleted tablet T-20 from the system permanently.','2026-03-13 18:18:05'),
(101,'Device Deleted','Sarinda','Admin deleted tablet T-19 from the system permanently.','2026-03-13 18:18:07'),
(102,'Device Force Unlocked','Sarinda','Admin unlocked tablet T-60.','2026-03-13 18:18:14'),
(103,'Device Force Unlocked','Sarinda','Admin unlocked tablet T-61.','2026-03-13 18:18:15'),
(104,'Device Force Unlocked','Sarinda','Admin unlocked tablet T-62.','2026-03-13 18:18:15'),
(105,'Device Edited','Sarinda','Admin updated data for tablet T-62.','2026-03-13 18:18:42'),
(106,'Device Edited','Sarinda','Admin updated data for tablet T-62.','2026-03-13 18:19:00'),
(107,'Device Edited','Sarinda','Admin updated data for tablet T-61.','2026-03-13 18:19:23'),
(108,'Device Deleted','Sarinda','Admin deleted tablet T-60 from the system permanently.','2026-03-13 18:19:36'),
(109,'Device Deleted','Sarinda','Admin deleted tablet T-61 from the system permanently.','2026-03-13 18:19:38'),
(110,'Device Edited','Sarinda','Admin updated data for tablet T-62.','2026-03-13 18:19:45'),
(111,'Device Deleted','Sarinda','Admin deleted tablet T-62 from the system permanently.','2026-03-13 18:20:17'),
(112,'Settings Updated','Sarinda','Batch target updated to 542.','2026-03-13 18:20:32'),
(113,'Settings Updated','Sarinda','Batch target updated to 542.','2026-03-13 18:20:33'),
(114,'Settings Updated','Sarinda','Batch target updated to 542.','2026-03-13 18:20:35'),
(115,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-13 18:24:01'),
(116,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-13 18:24:41'),
(117,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-13 18:25:34'),
(118,'Device Edited','Sarinda','Admin updated data for tablet T-64.','2026-03-13 18:28:00'),
(119,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-13 18:37:09'),
(120,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-13 18:38:34'),
(121,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-13 18:42:02'),
(122,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-13 18:43:13'),
(123,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-13 18:45:07'),
(124,'Settings Updated','Sarinda','Batch target updated to 100.','2026-03-13 18:45:21'),
(125,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-13 18:45:45'),
(126,'Settings Updated','Sarinda','Batch target updated to 10.','2026-03-13 18:55:46'),
(127,'Settings Updated','Sarinda','Batch target updated to 540.','2026-03-14 04:49:29'),
(128,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-14 04:49:40'),
(129,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-14 04:50:23'),
(130,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-14 04:54:22'),
(131,'User Login','Dhammika','User \'dhammika\' logged in successfully.','2026-03-14 04:54:29'),
(132,'User Logout','Dhammika','User \'dhammika\' logged out.','2026-03-14 04:55:55'),
(133,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-14 04:56:02'),
(134,'Device Edited','Sarinda','Admin updated data for tablet T-85.','2026-03-14 04:56:17'),
(135,'Device Edited','Sarinda','Admin updated data for tablet T-85.','2026-03-14 04:56:45'),
(136,'Device Edited','Sarinda','Admin updated data for tablet T-63.','2026-03-14 05:30:16'),
(137,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-14 05:57:32'),
(138,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-14 06:08:14'),
(139,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-14 06:11:08'),
(140,'User Login','Laksaman','User \'laksaman\' logged in successfully.','2026-03-14 06:11:18'),
(141,'Filtered Data Export','Laksaman','Exported filtered report. Filters - District: Colombo, Brand: Samsung, Status: All Statuses, Inspector: All Inspectors','2026-03-14 06:18:12'),
(142,'User Logout','Laksaman','User \'laksaman\' logged out.','2026-03-14 06:44:39'),
(143,'Accessories Export','Sarinda','Exported accessories detailed report to CSV.','2026-03-14 08:16:23'),
(144,'Device Force Unlocked','Sarinda','Admin unlocked tablet T-86.','2026-03-14 08:17:31'),
(145,'Accessories Export','Sarinda','Exported accessories detailed report to CSV.','2026-03-14 08:33:34'),
(146,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-14 08:40:37'),
(147,'Device Deleted','Sarinda','Admin deleted tablet T-63 from the system permanently.','2026-03-14 08:50:01'),
(148,'Device Deleted','Sarinda','Admin deleted tablet T-90 from the system permanently.','2026-03-14 08:50:08'),
(149,'Device Deleted','Sarinda','Admin deleted tablet T-88 from the system permanently.','2026-03-14 08:50:10'),
(150,'Device Deleted','Sarinda','Admin deleted tablet T-87 from the system permanently.','2026-03-14 08:50:12'),
(151,'Device Deleted','Sarinda','Admin deleted tablet T-85 from the system permanently.','2026-03-14 08:50:15'),
(152,'Device Deleted','Sarinda','Admin deleted tablet T-84 from the system permanently.','2026-03-14 08:50:17'),
(153,'Device Deleted','Sarinda','Admin deleted tablet T-83 from the system permanently.','2026-03-14 08:50:19'),
(154,'Device Deleted','Sarinda','Admin deleted tablet T-82 from the system permanently.','2026-03-14 08:50:21'),
(155,'Device Deleted','Sarinda','Admin deleted tablet T-81 from the system permanently.','2026-03-14 08:50:23'),
(156,'Device Deleted','Sarinda','Admin deleted tablet T-80 from the system permanently.','2026-03-14 08:50:25'),
(157,'Device Deleted','Sarinda','Admin deleted tablet T-79 from the system permanently.','2026-03-14 08:50:27'),
(158,'Device Deleted','Sarinda','Admin deleted tablet T-78 from the system permanently.','2026-03-14 08:50:29'),
(159,'Device Deleted','Sarinda','Admin deleted tablet T-77 from the system permanently.','2026-03-14 08:50:31'),
(160,'Device Deleted','Sarinda','Admin deleted tablet T-76 from the system permanently.','2026-03-14 08:50:33'),
(161,'Device Deleted','Sarinda','Admin deleted tablet T-75 from the system permanently.','2026-03-14 08:50:34'),
(162,'Device Deleted','Sarinda','Admin deleted tablet T-74 from the system permanently.','2026-03-14 08:50:36'),
(163,'Device Deleted','Sarinda','Admin deleted tablet T-73 from the system permanently.','2026-03-14 08:50:38'),
(164,'Device Deleted','Sarinda','Admin deleted tablet T-72 from the system permanently.','2026-03-14 08:50:40'),
(165,'Device Deleted','Sarinda','Admin deleted tablet T-71 from the system permanently.','2026-03-14 08:50:42'),
(166,'Device Deleted','Sarinda','Admin deleted tablet T-70 from the system permanently.','2026-03-14 08:50:44'),
(167,'Device Deleted','Sarinda','Admin deleted tablet T-69 from the system permanently.','2026-03-14 08:52:57'),
(168,'Device Deleted','Sarinda','Admin deleted tablet T-68 from the system permanently.','2026-03-14 08:53:01'),
(169,'Device Deleted','Sarinda','Admin deleted tablet T-67 from the system permanently.','2026-03-14 08:53:03'),
(170,'Device Deleted','Sarinda','Admin deleted tablet T-66 from the system permanently.','2026-03-14 08:53:05'),
(171,'Device Deleted','Sarinda','Admin deleted tablet T-65 from the system permanently.','2026-03-14 08:53:07'),
(172,'Device Deleted','Sarinda','Admin deleted tablet T-64 from the system permanently.','2026-03-14 08:53:10'),
(173,'Device Deleted','Sarinda','Admin deleted tablet T-89 from the system permanently.','2026-03-14 08:53:49'),
(174,'Device Deleted','Sarinda','Admin deleted tablet T-86 from the system permanently.','2026-03-14 08:53:51'),
(175,'Accessories Export','Sarinda','Exported accessories detailed report to CSV.','2026-03-14 09:05:55'),
(176,'Device Edited','Sarinda','Admin updated data for tablet T-91.','2026-03-14 09:07:10'),
(177,'Filtered Data Export','Sarinda','Exported filtered report. Filters - District: All Districts, Brand: All Brands, Status: All Statuses, Inspector: All Inspectors','2026-03-14 09:07:42'),
(178,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-14 09:08:25'),
(179,'Filtered Data Export','Sarinda','Exported filtered report. Filters - District: All Districts, Brand: All Brands, Status: All Statuses, Inspector: All Inspectors','2026-03-14 09:13:08'),
(180,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-14 09:35:19'),
(181,'Accessories Export','Sarinda','Exported accessories detailed report to CSV.','2026-03-14 09:35:35'),
(182,'Device Edited','Sarinda','Admin updated data for tablet T-92.','2026-03-14 09:37:12'),
(183,'Device Edited','Sarinda','Admin updated data for tablet T-92.','2026-03-14 09:37:32'),
(184,'Device Edited','Sarinda','Admin updated data for tablet T-92.','2026-03-14 09:37:57'),
(185,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-14 09:38:16'),
(186,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-14 09:46:48'),
(187,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-14 12:00:48'),
(188,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-14 12:01:31'),
(189,'User Login','Dhammika','User \'dhammika\' logged in successfully.','2026-03-14 12:01:39'),
(190,'User Logout','Dhammika','User \'dhammika\' logged out.','2026-03-14 12:02:19'),
(191,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-14 12:02:31'),
(192,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-14 12:03:12'),
(193,'User Login','Laksaman','User \'laksaman\' logged in successfully.','2026-03-14 12:03:24'),
(194,'User Logout','Laksaman','User \'laksaman\' logged out.','2026-03-14 12:03:39'),
(195,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-14 12:03:48'),
(196,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-14 12:05:40'),
(197,'User Created','Sarinda','Created new user \'sumith\' with role \'Technician\'.','2026-03-14 12:10:34'),
(198,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-14 12:11:44'),
(199,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-14 12:16:52'),
(200,'User Login','Dhammika','User \'dhammika\' logged in successfully.','2026-03-14 12:16:59'),
(201,'User Logout','Dhammika','User \'dhammika\' logged out.','2026-03-14 12:18:38'),
(202,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-14 12:18:47'),
(203,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-14 12:36:18'),
(204,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-14 12:36:30'),
(205,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-14 12:37:54'),
(206,'User Login','Dhammika','User \'dhammika\' logged in successfully.','2026-03-14 12:38:01'),
(207,'User Logout','Dhammika','User \'dhammika\' logged out.','2026-03-14 12:38:11'),
(208,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-14 12:38:21'),
(209,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-14 12:42:59'),
(210,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-14 13:59:26'),
(211,'Device Edited','Sarinda','Admin updated data for tablet T-92.','2026-03-14 14:01:42'),
(212,'Device Deleted','Sarinda','Admin deleted tablet T-96 from the system permanently.','2026-03-14 14:01:49'),
(213,'Device Deleted','Sarinda','Admin deleted tablet T-95 from the system permanently.','2026-03-14 14:01:52'),
(214,'Device Deleted','Sarinda','Admin deleted tablet T-94 from the system permanently.','2026-03-14 14:01:54'),
(215,'Device Deleted','Sarinda','Admin deleted tablet T-93 from the system permanently.','2026-03-14 14:01:56'),
(216,'Device Deleted','Sarinda','Admin deleted tablet T-92 from the system permanently.','2026-03-14 14:01:58'),
(217,'Device Deleted','Sarinda','Admin deleted tablet T-91 from the system permanently.','2026-03-14 14:02:00'),
(218,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-14 14:03:28'),
(219,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-14 14:13:05'),
(220,'Device Deleted','Sarinda','Admin deleted tablet T-97 from the system permanently.','2026-03-14 14:14:20'),
(221,'Device Deleted','Sarinda','Admin deleted tablet T-98 from the system permanently.','2026-03-14 14:15:55'),
(222,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-14 14:22:06'),
(223,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-14 14:22:19'),
(224,'Device Deleted','Sarinda','Admin deleted tablet T-99 from the system permanently.','2026-03-14 14:23:35'),
(225,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-14 14:23:44'),
(226,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-14 14:27:31'),
(227,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-14 14:27:35'),
(228,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-14 14:49:04'),
(229,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-14 14:49:12'),
(230,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-14 15:18:55'),
(231,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-14 15:19:33'),
(232,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-14 15:55:27'),
(233,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-14 15:57:12'),
(234,'User Login','Dhammika','User \'dhammika\' logged in successfully.','2026-03-14 15:57:24'),
(235,'User Logout','Dhammika','User \'dhammika\' logged out.','2026-03-14 15:57:26'),
(236,'User Login','Dhammika','User \'dhammika\' logged in successfully.','2026-03-14 15:57:37'),
(237,'User Logout','Dhammika','User \'dhammika\' logged out.','2026-03-14 16:06:22'),
(238,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-14 16:07:09'),
(239,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-14 16:18:47'),
(240,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-14 17:01:24'),
(241,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-14 17:01:28'),
(242,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-14 17:02:09'),
(243,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-14 17:02:13'),
(244,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-14 17:05:37'),
(245,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-14 17:05:43'),
(246,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-14 17:06:00'),
(247,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-14 17:06:13'),
(248,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-14 17:12:05'),
(249,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-14 17:12:17'),
(250,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-14 17:30:29'),
(251,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-14 17:30:35'),
(252,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-14 17:36:17'),
(253,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-14 17:36:20'),
(254,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-14 17:40:06'),
(255,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-14 17:40:10'),
(256,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-14 17:40:50'),
(257,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-14 17:40:56'),
(258,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-14 17:41:00'),
(259,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-14 17:41:02'),
(260,'User Login','Sarinda','User \'admin\' logged in successfully.','2026-03-14 17:42:34'),
(261,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-14 17:42:39'),
(262,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-14 17:42:39'),
(263,'Device Edited','Sarinda','Admin updated data for tablet T-102.','2026-03-14 18:22:34'),
(264,'Device Deleted','Sarinda','Deleted T-102','2026-03-14 18:48:03'),
(265,'User Logout','Sarinda','User logged out.','2026-03-14 18:51:31'),
(266,'User Login','Sarinda','User \'admin\' logged in.','2026-03-14 18:51:34'),
(267,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-14 19:07:53'),
(268,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-14 19:12:49'),
(269,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-14 19:13:03'),
(270,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-14 19:29:07'),
(271,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-15 01:08:29'),
(272,'User Login','Sarinda','User \'admin\' logged in.','2026-03-15 01:08:36'),
(273,'Device Edited','Sarinda','Admin updated data for tablet T-104.','2026-03-15 01:09:55'),
(274,'Accessories Export','Sarinda','Exported accessories detailed report to CSV.','2026-03-15 01:10:04'),
(275,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-15 01:10:53'),
(276,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-15 01:15:01'),
(277,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-15 01:19:41'),
(278,'User Login','Sarinda','User \'admin\' logged in.','2026-03-15 02:26:12'),
(279,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-15 02:37:58'),
(280,'User Login','Dhammika','User \'dhammika\' logged in.','2026-03-15 02:39:25'),
(281,'User Logout','Dhammika','User \'dhammika\' logged out.','2026-03-15 02:39:52'),
(282,'User Login','Sarinda','User \'admin\' logged in.','2026-03-15 04:37:59'),
(283,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-15 05:44:02'),
(284,'User Login','Sarinda','User \'admin\' logged in.','2026-03-15 05:44:05'),
(285,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-15 07:13:37'),
(286,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-15 07:31:16'),
(287,'User Login','Sarinda','User \'admin\' logged in.','2026-03-15 07:49:21'),
(288,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-15 07:49:53'),
(289,'User Login','Sarinda','User \'admin\' logged in.','2026-03-15 07:58:54'),
(290,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-15 07:58:59'),
(291,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-15 08:01:56'),
(292,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-15 08:03:35'),
(293,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-15 08:04:14'),
(294,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-15 08:17:46'),
(295,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-15 08:18:00'),
(296,'Device Edited','Sarinda','Admin updated data for tablet T-3.','2026-03-15 09:19:39'),
(297,'Device Edited','Sarinda','Admin updated data for tablet T-2.','2026-03-15 09:20:08'),
(298,'Device Edited','Sarinda','Admin updated data for tablet T-1.','2026-03-15 09:20:53'),
(299,'Device Edited','Sarinda','Admin updated data for tablet T-3.','2026-03-15 10:30:58'),
(300,'Device Edited','Sarinda','Admin updated data for tablet T-2.','2026-03-15 10:31:23'),
(301,'Device Edited','Sarinda','Admin updated data for tablet T-1.','2026-03-15 10:31:39'),
(302,'Device Edited','Sarinda','Admin updated data for tablet T-3.','2026-03-15 10:32:13'),
(303,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-15 10:32:52'),
(304,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-15 10:33:15'),
(305,'Device Force Unlocked','Sarinda','Admin unlocked tablet T-4.','2026-03-15 10:40:34'),
(306,'Device Edited','Sarinda','Admin updated data for tablet T-3.','2026-03-15 10:58:44'),
(307,'Device Edited','Sarinda','Admin updated data for tablet T-3.','2026-03-15 11:00:10'),
(308,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-15 11:21:40'),
(309,'Device Edited','Sarinda','Admin updated data for tablet T-8.','2026-03-15 11:23:09'),
(310,'Device Edited','Sarinda','Admin updated data for tablet T-8.','2026-03-15 11:34:44'),
(311,'Device Edited','Sarinda','Admin updated data for tablet T-8.','2026-03-15 11:35:03'),
(312,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-15 11:40:33'),
(313,'User Login','Sarinda','User \'admin\' logged in.','2026-03-15 11:40:37'),
(314,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-15 11:42:29'),
(315,'User Login','Dhammika','User \'dhammika\' logged in.','2026-03-15 11:42:32'),
(316,'User Logout','Dhammika','User \'dhammika\' logged out.','2026-03-15 11:44:45'),
(317,'User Login','kosala','User \'kosala\' logged in.','2026-03-15 11:44:57'),
(318,'User Logout','kosala','User \'kosala\' logged out.','2026-03-15 11:45:43'),
(319,'User Login','Laksaman','User \'laksaman\' logged in.','2026-03-15 11:45:54'),
(320,'User Logout','Laksaman','User \'laksaman\' logged out.','2026-03-15 11:51:47'),
(321,'User Login','Sarinda','User \'admin\' logged in.','2026-03-15 11:51:50'),
(322,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-15 12:13:10'),
(323,'User Login','Sarinda','User \'admin\' logged in.','2026-03-15 12:23:52'),
(324,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-15 12:25:38'),
(325,'User Login','Sarinda','User \'admin\' logged in.','2026-03-15 12:57:24'),
(326,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-15 12:59:40'),
(327,'Device Edited','Sarinda','Admin updated data for tablet T-12.','2026-03-15 14:49:30'),
(328,'Device Edited','Sarinda','Admin updated data for tablet T-11.','2026-03-15 14:50:07'),
(329,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-15 15:06:18'),
(330,'Device Edited','Sarinda','Admin updated data for tablet T-12.','2026-03-15 15:06:48'),
(331,'Device Edited','Sarinda','Admin updated data for tablet T-12.','2026-03-15 15:07:16'),
(332,'Device Edited','Sarinda','Admin updated data for tablet T-11.','2026-03-15 15:07:39'),
(333,'Device Edited','Sarinda','Admin updated data for tablet T-10.','2026-03-15 15:07:56'),
(334,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-15 15:18:06'),
(335,'User Login','Sarinda','User \'admin\' logged in.','2026-03-15 15:35:37'),
(336,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-15 15:35:45'),
(337,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-15 15:36:14'),
(338,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-15 16:08:26'),
(339,'User Created','Sarinda','Created new user \'ict\' with role \'Technician\'.','2026-03-15 16:09:13'),
(340,'Password Reset','Sarinda','Admin reset password for user \'ict\'.','2026-03-15 16:09:27'),
(341,'User Deleted','Sarinda','Deleted user \'ict\'.','2026-03-15 16:09:38'),
(342,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-15 16:15:25'),
(343,'Device Edited','Sarinda','Admin updated data for tablet T-12.','2026-03-15 16:16:37'),
(344,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-15 16:17:02'),
(345,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-15 16:19:25'),
(346,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-15 16:45:07'),
(347,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-15 16:46:48'),
(348,'User Login','Sarinda','User \'admin\' logged in.','2026-03-15 18:22:44'),
(349,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-15 18:24:38'),
(350,'User Login','Dhammika','User \'dhammika\' logged in.','2026-03-15 18:24:48'),
(351,'User Login','Laksaman','User \'laksaman\' logged in.','2026-03-15 18:27:02'),
(352,'User Logout','Dhammika','User \'dhammika\' logged out.','2026-03-15 18:28:55'),
(353,'User Login','Sarinda','User \'admin\' logged in.','2026-03-15 18:29:07'),
(354,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-15 18:33:19'),
(355,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-16 01:30:51'),
(356,'User Login','Sarinda','User \'admin\' logged in.','2026-03-16 01:31:15'),
(357,'User Login','Sarinda','User \'admin\' logged in.','2026-03-16 01:31:17'),
(358,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-16 01:31:35'),
(359,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-16 01:41:16'),
(360,'User Login','Sarinda','User \'admin\' logged in.','2026-03-16 05:22:28'),
(361,'Device Edited','Sarinda','Admin updated data for tablet T-3.','2026-03-16 06:06:26'),
(362,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-16 06:07:57'),
(363,'User Login','Sarinda','User \'admin\' logged in.','2026-03-16 06:23:05'),
(364,'User Login','Sarinda','User \'admin\' logged in.','2026-03-16 06:40:13'),
(365,'Device Force Unlocked','Sarinda','Admin unlocked tablet T-2.','2026-03-16 06:45:21'),
(366,'Device Deleted','Sarinda','Admin deleted tablet T-2 from the system permanently.','2026-03-16 07:09:10'),
(367,'Device Deleted','Sarinda','Admin deleted tablet T-1 from the system permanently.','2026-03-16 07:09:13'),
(368,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-16 07:11:00'),
(369,'Device Deleted','Sarinda','Admin deleted tablet T-4 from the system permanently.','2026-03-16 07:11:32'),
(370,'Device Deleted','Sarinda','Admin deleted tablet T-3 from the system permanently.','2026-03-16 07:11:34'),
(371,'Device Edited','Sarinda','Admin updated data for tablet T-5.','2026-03-16 07:12:49'),
(372,'Device Edited','Sarinda','Admin updated data for tablet T-5.','2026-03-16 07:12:57'),
(373,'Device Deleted','Sarinda','Admin deleted tablet T-5 from the system permanently.','2026-03-16 07:13:05'),
(374,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-16 07:18:47'),
(375,'Device Edited','Sarinda','Admin updated data for tablet T-7.','2026-03-16 07:19:42'),
(376,'Accessories Export','Sarinda','Exported accessories detailed report to CSV.','2026-03-16 07:19:52'),
(377,'Device Deleted','Sarinda','Admin deleted tablet T-7 from the system permanently.','2026-03-16 07:21:05'),
(378,'Device Deleted','Sarinda','Admin deleted tablet T-6 from the system permanently.','2026-03-16 07:21:07'),
(379,'Device Edited','Sarinda','Admin updated data for tablet T-3.','2026-03-16 07:24:40'),
(380,'Device Edited','Sarinda','Admin updated data for tablet T-3.','2026-03-16 07:24:59'),
(381,'Device Edited','Sarinda','Admin updated data for tablet T-4.','2026-03-16 07:29:34'),
(382,'Device Deleted','Sarinda','Admin deleted tablet T-1 from the system permanently.','2026-03-16 07:29:57'),
(383,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-16 07:31:39'),
(384,'Device Edited','Sarinda','Admin updated data for tablet T-3.','2026-03-16 07:33:14'),
(385,'Device Deleted','Sarinda','Admin deleted tablet T-2 from the system permanently.','2026-03-16 07:38:26'),
(386,'Device Deleted','Sarinda','Admin deleted tablet T-3 from the system permanently.','2026-03-16 07:38:28'),
(387,'Device Edited','Sarinda','Admin updated data for tablet T-5.','2026-03-16 08:29:13'),
(388,'Device Edited','Sarinda','Admin updated data for tablet T-5.','2026-03-16 08:29:31'),
(389,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-16 08:49:01'),
(390,'Device Edited','Sarinda','Admin updated data for tablet T-1.','2026-03-16 08:50:46'),
(391,'Device Edited','Sarinda','Admin updated data for tablet T-1.','2026-03-16 08:51:07'),
(392,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-16 09:51:53'),
(393,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-16 09:53:13'),
(394,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-16 09:55:26'),
(395,'User Login','Laksaman','User \'laksaman\' logged in.','2026-03-16 09:55:59'),
(396,'User Logout','Laksaman','User \'laksaman\' logged out.','2026-03-16 10:23:53'),
(397,'User Login','Sarinda','User \'admin\' logged in.','2026-03-16 10:24:00'),
(398,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-16 10:24:15'),
(399,'User Login','Sarinda','User \'admin\' logged in.','2026-03-17 03:16:11'),
(400,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-17 03:18:24'),
(401,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-17 03:19:01'),
(402,'User Login','Dhammika','User \'dhammika\' logged in.','2026-03-17 03:19:10'),
(403,'Filtered Data Export','Dhammika','Exported filtered report.','2026-03-17 03:19:17'),
(404,'User Logout','Dhammika','User \'dhammika\' logged out.','2026-03-17 03:31:56'),
(405,'User Login','Dhammika','User \'dhammika\' logged in.','2026-03-17 03:32:04'),
(406,'User Logout','Dhammika','User \'dhammika\' logged out.','2026-03-17 03:32:41'),
(407,'User Login','Sarinda','User \'admin\' logged in.','2026-03-17 03:32:50'),
(408,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-17 03:33:05'),
(409,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-17 03:37:16'),
(410,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-17 03:42:39'),
(411,'User Login','Dhammika','User \'dhammika\' logged in.','2026-03-17 03:42:47'),
(412,'User Logout','Dhammika','User \'dhammika\' logged out.','2026-03-17 03:43:32'),
(413,'User Login','Sarinda','User \'admin\' logged in.','2026-03-17 03:43:40'),
(414,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-17 03:44:30'),
(415,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-17 03:45:43'),
(416,'Device Edited','Sarinda','Admin updated data for tablet T-2.','2026-03-17 06:19:15'),
(417,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-17 06:32:58'),
(418,'User Login','Sarinda','User \'admin\' logged in.','2026-03-17 06:36:33'),
(419,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-17 06:36:36'),
(420,'User Login','Sarinda','User \'admin\' logged in.','2026-03-17 06:36:46'),
(421,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-17 06:46:18'),
(422,'User Login','Sarinda','User \'admin\' logged in.','2026-03-17 07:37:26'),
(423,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-17 08:04:58'),
(424,'User Login','Sarinda','User \'admin\' logged in.','2026-03-17 08:05:13'),
(425,'User Login','Sarinda','User \'admin\' logged in.','2026-03-19 03:40:14'),
(426,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-19 06:29:22'),
(427,'Device Deleted','Sarinda','Admin deleted tablet T-1 from the system permanently.','2026-03-19 06:31:00'),
(428,'Device Deleted','Sarinda','Admin deleted tablet T-2 from the system permanently.','2026-03-19 10:21:25'),
(429,'Device Deleted','Sarinda','Admin deleted tablet T-2 from the system permanently.','2026-03-19 10:22:11'),
(430,'Device Deleted','Sarinda','Admin deleted tablet T-3 from the system permanently.','2026-03-19 10:23:10'),
(431,'Device Deleted','Sarinda','Admin deleted tablet T-3 from the system permanently.','2026-03-19 10:23:18'),
(432,'User Login','Sarinda','User \'admin\' logged in.','2026-03-20 05:06:18'),
(433,'Device Deleted','Sarinda','Admin deleted tablet T-2 from the system permanently.','2026-03-20 05:06:24'),
(434,'Device Deleted','Sarinda','Admin deleted tablet T-4 from the system permanently.','2026-03-20 05:20:33'),
(435,'Device Deleted','Sarinda','Admin deleted tablet T-5 from the system permanently.','2026-03-20 05:20:36'),
(436,'Device Restored','Sarinda','Admin restored tablet T-5 from Trash Bin.','2026-03-20 05:20:43'),
(437,'Device Restored','Sarinda','Admin restored tablet T-2 from Trash Bin.','2026-03-20 05:20:44'),
(438,'Device Restored','Sarinda','Admin restored tablet T-3 from Trash Bin.','2026-03-20 05:20:45'),
(439,'Device Restored','Sarinda','Admin restored tablet T-4 from Trash Bin.','2026-03-20 05:20:45'),
(440,'Device Edited','Sarinda','Admin updated data for tablet T-5.','2026-03-20 05:21:07'),
(441,'Device Deleted','Sarinda','Admin deleted tablet T-2 from the system permanently.','2026-03-20 05:21:49'),
(442,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-20 05:23:39'),
(443,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-20 05:35:44'),
(444,'User Login','Sarinda','User \'admin\' logged in.','2026-03-20 05:35:55'),
(445,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-20 05:38:18'),
(446,'User Login','Sarinda','User \'admin\' logged in.','2026-03-20 05:50:26'),
(447,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-20 05:54:47'),
(448,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-20 06:02:45'),
(449,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-20 06:02:51'),
(450,'User Login','Sarinda','User \'admin\' logged in.','2026-03-20 06:03:01'),
(451,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-20 06:04:10'),
(452,'Device Restored','Sarinda','Admin restored tablet T-2 from Trash Bin.','2026-03-20 07:00:52'),
(453,'Device Deleted','Sarinda','Admin deleted tablet T-12 from the system permanently.','2026-03-20 07:01:00'),
(454,'Device Restored','Sarinda','Admin restored tablet T-12 from Trash Bin.','2026-03-20 07:01:05'),
(455,'Device Deleted','Sarinda','Admin deleted tablet T-12 from the system permanently.','2026-03-20 07:01:15'),
(456,'Device Restored','Sarinda','Admin restored tablet T-12 from Trash Bin.','2026-03-20 07:01:24'),
(457,'Device Deleted','Sarinda','Admin deleted tablet T-4 from the system permanently.','2026-03-20 07:01:50'),
(458,'Device Restored','Sarinda','Admin restored tablet T-4 from Trash Bin.','2026-03-20 07:02:16'),
(459,'Device Deleted','Sarinda','Admin deleted tablet T-4 from the system permanently.','2026-03-20 07:02:27'),
(460,'Device Restored','Sarinda','Admin restored tablet T-4 from Trash Bin.','2026-03-20 07:42:21'),
(461,'Device Deleted','Sarinda','Admin deleted tablet T-4 from the system permanently.','2026-03-20 07:42:33'),
(462,'Device Edited','Sarinda','Admin updated data for tablet T-12.','2026-03-20 07:43:06'),
(463,'Device Deleted','Sarinda','Admin deleted tablet T-12 from the system permanently.','2026-03-20 07:43:31'),
(464,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-20 10:38:58'),
(465,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-20 10:40:01'),
(466,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-20 10:46:25'),
(467,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-20 11:26:56'),
(468,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-20 11:29:48'),
(469,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-20 12:03:04'),
(470,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-20 12:03:45'),
(471,'Device Edited','Sarinda','Admin updated data for tablet T-6.','2026-03-20 12:05:43'),
(472,'User Login','Sarinda','User \'admin\' logged in.','2026-03-20 12:30:23'),
(473,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-20 12:31:00'),
(474,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-20 12:32:45'),
(475,'User Login','kosala','User \'kosala\' logged in.','2026-03-20 12:32:48'),
(476,'User Login','Sarinda','User \'admin\' logged in.','2026-03-20 13:58:08'),
(477,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-20 14:00:06'),
(478,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-20 14:00:49'),
(479,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-20 14:01:13'),
(480,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-20 14:01:33'),
(481,'Device Edited','Sarinda','Admin updated data for tablet T-7.','2026-03-20 14:02:07'),
(482,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-20 14:02:27'),
(483,'Device Edited','Sarinda','Admin updated data for tablet T-7.','2026-03-20 14:03:12'),
(484,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-20 14:03:17'),
(485,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-20 14:47:06'),
(486,'Device Edited','Sarinda','Admin updated data for tablet T-12.','2026-03-20 14:53:59'),
(487,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-20 15:02:40'),
(488,'User Login','Sarinda','User \'admin\' logged in.','2026-03-20 15:02:47'),
(489,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-20 15:22:31'),
(490,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-20 15:22:58'),
(491,'Device Edited','Sarinda','Admin updated data for tablet T-7.','2026-03-20 15:24:07'),
(492,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-20 15:24:19'),
(493,'Device Deleted','Sarinda','Admin deleted tablet T-1 from the system permanently.','2026-03-20 15:25:54'),
(494,'Device Restored','Sarinda','Admin restored tablet T-1 from Trash Bin.','2026-03-20 15:25:59'),
(495,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-20 15:30:31'),
(496,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-20 15:47:16'),
(497,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-20 16:11:35'),
(498,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-20 17:48:48'),
(499,'User Login','Sarinda','User \'admin\' logged in.','2026-03-20 17:48:51'),
(500,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-20 17:58:01'),
(501,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-20 18:36:16'),
(502,'Device Edited','Sarinda','Admin updated data for tablet T-7.','2026-03-20 18:37:50'),
(503,'Device Edited','Sarinda','Admin updated data for tablet T-7.','2026-03-20 18:38:09'),
(504,'Device Deleted','Sarinda','Admin deleted tablet T-1 from the system permanently.','2026-03-20 18:38:23'),
(505,'Device Restored','Sarinda','Admin restored tablet T-1 from Trash Bin.','2026-03-20 18:38:28'),
(506,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-20 18:52:45'),
(507,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-20 19:00:40'),
(508,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-21 05:47:20'),
(509,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-21 06:07:20'),
(510,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-21 06:20:03'),
(511,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-21 06:21:08'),
(512,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-21 06:33:12'),
(513,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-21 06:39:02'),
(514,'Device Deleted','Sarinda','Admin deleted tablet T-1 from the system permanently.','2026-03-21 07:01:05'),
(515,'Device Restored','Sarinda','Admin restored tablet T-1 from Trash Bin.','2026-03-21 07:01:11'),
(516,'Device Deleted','Sarinda','Admin deleted tablet T-1 from the system permanently.','2026-03-21 07:03:19'),
(517,'Device Restored','Sarinda','Admin restored tablet T-1 from Trash Bin.','2026-03-21 07:03:42'),
(518,'Device Deleted','Sarinda','Admin deleted tablet T-1 from the system permanently.','2026-03-21 07:03:51'),
(519,'Device Restored','Sarinda','Admin restored tablet T-1 from Trash Bin.','2026-03-21 07:04:07'),
(520,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-21 07:47:14'),
(521,'User Login','kosala','User \'kosala\' logged in.','2026-03-21 07:47:18'),
(522,'User Logout','kosala','User \'kosala\' logged out.','2026-03-21 07:48:48'),
(523,'User Login','kosala','User \'kosala\' logged in.','2026-03-21 07:48:52'),
(524,'User Logout','kosala','User \'kosala\' logged out.','2026-03-21 07:48:57'),
(525,'User Login','Sarinda','User \'admin\' logged in.','2026-03-21 07:49:01'),
(526,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-21 07:53:09'),
(527,'User Login','Dhammika','User \'dhammika\' logged in.','2026-03-21 07:53:13'),
(528,'User Logout','Dhammika','User \'dhammika\' logged out.','2026-03-21 08:12:17'),
(529,'User Login','Sarinda','User \'admin\' logged in.','2026-03-21 08:12:20'),
(530,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-21 08:14:26'),
(531,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-21 08:15:11'),
(532,'User Login','Dhammika','User \'dhammika\' logged in.','2026-03-21 08:15:14'),
(533,'Filtered Data Export','Dhammika','Exported filtered report.','2026-03-21 08:17:08'),
(534,'User Logout','Dhammika','User \'dhammika\' logged out.','2026-03-21 08:18:49'),
(535,'User Login','Sarinda','User \'admin\' logged in.','2026-03-21 08:18:53'),
(536,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-21 08:19:03'),
(537,'User Login','kosala','User \'kosala\' logged in.','2026-03-21 08:19:06'),
(538,'User Logout','kosala','User \'kosala\' logged out.','2026-03-21 08:35:39'),
(539,'User Login','Sarinda','User \'admin\' logged in.','2026-03-21 08:35:43'),
(540,'Device Deleted','Sarinda','Admin deleted tablet T-1 from the system permanently.','2026-03-21 09:12:19'),
(541,'Device Restored','Sarinda','Admin restored tablet T-1 from Trash Bin.','2026-03-21 09:12:25'),
(542,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-21 09:14:07'),
(543,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-21 09:14:58'),
(544,'User Login','Dhammika','User \'dhammika\' logged in.','2026-03-21 09:15:01'),
(545,'Filtered Data Export','Dhammika','Exported filtered report.','2026-03-21 09:20:06'),
(546,'Filtered Data Export','Dhammika','Exported filtered report.','2026-03-21 09:21:37'),
(547,'User Logout','Dhammika','User \'dhammika\' logged out.','2026-03-21 09:31:55'),
(548,'User Login','Sarinda','User \'admin\' logged in.','2026-03-21 09:32:06'),
(549,'Device Force Unlocked','Sarinda','Admin unlocked tablet T-18.','2026-03-21 09:32:24'),
(550,'Device Edited','Sarinda','Admin updated data for tablet T-18.','2026-03-21 09:33:11'),
(551,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-21 09:34:09'),
(552,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-21 11:06:34'),
(553,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-21 11:07:08'),
(554,'Device Edited','Sarinda','Admin updated data for tablet T-20.','2026-03-21 11:09:19'),
(555,'Device Deleted','Sarinda','Admin deleted tablet T-20 from the system permanently.','2026-03-21 11:09:36'),
(556,'Device Restored','Sarinda','Admin restored tablet T-20 from Trash Bin.','2026-03-21 11:09:50'),
(557,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-21 11:27:29'),
(558,'User Login','Sarinda','User \'admin\' logged in.','2026-03-21 11:27:41'),
(559,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-21 11:27:51'),
(560,'User Login','Sarinda','User \'admin\' logged in.','2026-03-21 11:27:54'),
(561,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-21 11:28:00'),
(562,'User Login','Sarinda','User \'admin\' logged in.','2026-03-21 11:28:25'),
(563,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-21 11:29:54'),
(564,'User Login','kosala','User \'kosala\' logged in.','2026-03-21 11:29:57'),
(565,'User Login','Sarinda','User \'admin\' logged in.','2026-03-21 11:39:20'),
(566,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-21 11:41:05'),
(567,'User Logout','kosala','User \'kosala\' logged out.','2026-03-21 11:41:52'),
(568,'User Login','Sarinda','User \'admin\' logged in.','2026-03-21 11:41:55'),
(569,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-21 12:00:06'),
(570,'User Login','Sarinda','User \'admin\' logged in.','2026-03-21 12:00:10'),
(571,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-21 12:00:18'),
(572,'User Login','kosala','User \'kosala\' logged in.','2026-03-21 12:00:21'),
(573,'User Logout','kosala','User \'kosala\' logged out.','2026-03-21 12:00:29'),
(574,'User Login','Sarinda','User \'admin\' logged in.','2026-03-21 12:00:33'),
(575,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-21 12:01:00'),
(576,'User Login','Sarinda','User \'admin\' logged in.','2026-03-21 12:01:04'),
(577,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-21 12:04:15'),
(578,'User Login','Sarinda','User \'admin\' logged in.','2026-03-21 12:04:18'),
(579,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-21 12:08:36'),
(580,'User Login','Laksaman','User \'laksaman\' logged in.','2026-03-21 12:09:01'),
(581,'User Logout','Laksaman','User \'laksaman\' logged out.','2026-03-21 12:10:58'),
(582,'User Login','Laksaman','User \'laksaman\' logged in.','2026-03-21 12:11:03'),
(583,'User Logout','Laksaman','User \'laksaman\' logged out.','2026-03-21 12:11:36'),
(584,'User Login','Sarinda','User \'admin\' logged in.','2026-03-21 12:11:39'),
(585,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-21 12:11:47'),
(586,'User Login','Laksaman','User \'laksaman\' logged in.','2026-03-21 12:11:50'),
(587,'User Logout','Laksaman','User \'laksaman\' logged out.','2026-03-21 12:12:48'),
(588,'User Login','Sarinda','User \'admin\' logged in.','2026-03-21 12:12:51'),
(589,'Settings Updated','Sarinda','Admin updated System Settings & District Targets.','2026-03-21 12:13:50'),
(590,'Settings Updated','Sarinda','Admin updated System Settings & District Targets.','2026-03-21 12:14:17'),
(591,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-21 12:14:22'),
(592,'User Login','Sarinda','User \'admin\' logged in.','2026-03-21 12:14:26'),
(593,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-21 12:21:16'),
(594,'User Login','Dhammika','User \'dhammika\' logged in.','2026-03-21 12:21:21'),
(595,'Filtered Data Export','Dhammika','Exported filtered report.','2026-03-21 12:21:47'),
(596,'User Logout','Dhammika','User \'dhammika\' logged out.','2026-03-21 12:23:14'),
(597,'User Login','Sarinda','User \'admin\' logged in.','2026-03-21 12:23:17'),
(598,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-21 12:23:36'),
(599,'User Login','Dhammika','User \'dhammika\' logged in.','2026-03-21 12:23:40'),
(600,'User Logout','Dhammika','User \'dhammika\' logged out.','2026-03-21 12:28:38'),
(601,'User Login','Sarinda','User \'admin\' logged in.','2026-03-21 13:10:08'),
(602,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-21 13:10:14'),
(603,'User Login','Dhammika','User \'dhammika\' logged in.','2026-03-21 13:10:32'),
(604,'User Logout','Dhammika','User \'dhammika\' logged out.','2026-03-21 13:59:24'),
(605,'User Login','Sarinda','User \'admin\' logged in.','2026-03-21 13:59:28'),
(606,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-21 13:59:56'),
(607,'User Login','Sarinda','User \'admin\' logged in.','2026-03-21 14:00:00'),
(608,'Device Edited','Sarinda','Admin updated data for tablet T-58.','2026-03-21 14:19:44'),
(609,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-21 14:28:55'),
(610,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-21 14:36:49'),
(611,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-21 15:11:58'),
(612,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-21 15:13:11'),
(613,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-21 15:43:13'),
(614,'Accessories Export','Sarinda','Exported accessories detailed report to CSV.','2026-03-21 17:21:29'),
(615,'Device Deleted','Sarinda','Admin deleted tablet T-60 from the system permanently.','2026-03-21 17:31:15'),
(616,'Device Restored','Sarinda','Admin restored tablet T-60 from Trash Bin.','2026-03-21 17:32:04'),
(617,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-21 17:44:12'),
(618,'Accessories Export','Sarinda','Exported accessories detailed report to CSV.','2026-03-21 17:46:19'),
(619,'Device Edited','Sarinda','Admin updated data for tablet T-60.','2026-03-21 17:46:44'),
(620,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-21 17:53:39'),
(621,'Device Force Unlocked','Sarinda','Admin unlocked tablet T-17.','2026-03-21 18:01:22'),
(622,'User Login','Sarinda','User \'admin\' logged in.','2026-03-21 18:07:17'),
(623,'Device Edited','Sarinda','Admin updated data for tablet T-60.','2026-03-21 18:14:26'),
(624,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-21 18:15:11'),
(625,'Device Edited','Sarinda','Admin updated data for tablet T-60.','2026-03-21 18:16:55'),
(626,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-21 18:17:55'),
(627,'Accessories Export','Sarinda','Exported accessories detailed report to CSV.','2026-03-21 18:18:30'),
(628,'User Login','Sarinda','User \'admin\' logged in.','2026-03-21 18:21:46'),
(629,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-21 18:22:09'),
(630,'Device Deleted','Sarinda','Admin deleted tablet T-61 from the system permanently.','2026-03-21 18:25:25'),
(631,'Device Restored','Sarinda','Admin restored tablet T-61 from Trash Bin.','2026-03-21 18:25:34'),
(632,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-21 18:26:48'),
(633,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-21 18:28:52'),
(634,'User Login','Sarinda','User \'admin\' logged in.','2026-03-21 18:46:51'),
(635,'Device Edited','Sarinda','Admin updated data for tablet T-59.','2026-03-21 18:47:43'),
(636,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-21 18:49:40'),
(637,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-21 18:51:53'),
(638,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-21 19:24:37'),
(639,'Device Deleted','Sarinda','Admin deleted tablet T-61 from the system permanently.','2026-03-21 19:25:17'),
(640,'Device Restored','Sarinda','Admin restored tablet T-61 from Trash Bin.','2026-03-21 19:25:22'),
(641,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-21 19:25:23'),
(642,'User Login','Dhammika','User \'dhammika\' logged in.','2026-03-21 19:25:27'),
(643,'User Logout','Dhammika','User \'dhammika\' logged out.','2026-03-21 19:25:29'),
(644,'User Login','Sarinda','User \'admin\' logged in.','2026-03-21 19:25:35'),
(645,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-21 19:27:11'),
(646,'User Login','Sarinda','User \'admin\' logged in.','2026-03-22 00:38:35'),
(647,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-22 01:04:43'),
(648,'Accessories Export','Sarinda','Exported accessories detailed report to CSV.','2026-03-22 01:47:08'),
(649,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-22 01:49:06'),
(650,'User Login','Sarinda','User \'admin\' logged in.','2026-03-22 01:49:10'),
(651,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-22 01:49:15'),
(652,'User Login','Dhammika','User \'dhammika\' logged in.','2026-03-22 01:49:53'),
(653,'User Logout','Dhammika','User \'dhammika\' logged out.','2026-03-22 01:53:59'),
(654,'User Login','Sarinda','User \'admin\' logged in.','2026-03-22 01:54:03'),
(655,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-22 01:54:56'),
(656,'Accessories Export','Sarinda','Exported accessories detailed report to CSV.','2026-03-22 01:56:54'),
(657,'Device Edited','Sarinda','Admin updated data for tablet T-61.','2026-03-22 01:57:55'),
(658,'Device Edited','Sarinda','Admin updated data for tablet T-61.','2026-03-22 01:58:36'),
(659,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-22 01:59:08'),
(660,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-22 02:03:12'),
(661,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-22 02:35:25'),
(662,'User Login','Sarinda','User \'admin\' logged in.','2026-03-23 03:10:47'),
(663,'User Created','Sarinda','Created new user \'tempadmin\' with role \'Admin\'.','2026-03-23 03:11:45'),
(664,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-23 03:11:50'),
(665,'User Login','Tempadmin','User \'tempadmin\' logged in.','2026-03-23 03:12:08'),
(666,'User Logout','Tempadmin','User \'tempadmin\' logged out.','2026-03-23 03:12:41'),
(667,'User Login','Tempadmin','User \'tempadmin\' logged in.','2026-03-23 04:05:55'),
(668,'Filtered Data Export','Tempadmin','Exported filtered report.','2026-03-23 04:36:44'),
(669,'Device Edited','Tempadmin','Admin updated data for tablet T-2.','2026-03-23 04:38:55'),
(670,'Device Edited','Tempadmin','Admin updated data for tablet T-1.','2026-03-23 04:39:38'),
(671,'Filtered Data Export','Tempadmin','Exported filtered report.','2026-03-23 04:40:12'),
(672,'Device Edited','Tempadmin','Admin updated data for tablet T-1.','2026-03-23 04:40:35'),
(673,'Device Edited','Tempadmin','Admin updated data for tablet T-2.','2026-03-23 04:41:13'),
(674,'Filtered Data Export','Tempadmin','Exported filtered report.','2026-03-23 04:41:29'),
(675,'Device Edited','Tempadmin','Admin updated data for tablet T-1.','2026-03-23 04:41:57'),
(676,'Filtered Data Export','Tempadmin','Exported filtered report.','2026-03-23 04:42:34'),
(677,'Device Edited','Tempadmin','Admin updated data for tablet T-1.','2026-03-23 04:44:24'),
(678,'Filtered Data Export','Tempadmin','Exported filtered report.','2026-03-23 04:44:53'),
(679,'Data Export','Tempadmin','Exported full tablet database to CSV.','2026-03-23 04:53:55'),
(680,'User Login','Sarinda','User \'admin\' logged in.','2026-03-23 08:59:58'),
(681,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-23 10:26:11'),
(682,'Device Deleted','Sarinda','Admin deleted tablet T-61 from the system permanently.','2026-03-23 10:27:34'),
(683,'Device Restored','Sarinda','Admin restored tablet T-61 from Trash Bin.','2026-03-23 10:27:38'),
(684,'User Login','Sarinda','User \'admin\' logged in.','2026-03-24 03:02:16'),
(685,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-24 03:10:55'),
(686,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-24 06:34:18'),
(687,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-24 06:34:38'),
(688,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-24 06:34:57'),
(689,'Filtered Data Export','Sarinda','Exported filtered report.','2026-03-24 06:35:35'),
(690,'Device Deleted','Sarinda','Admin deleted tablet T-61 from the system permanently.','2026-03-24 06:37:15'),
(691,'Device Restored','Sarinda','Admin restored tablet T-61 from Trash Bin.','2026-03-24 06:37:18'),
(692,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-24 07:24:29'),
(693,'User Login','Dhammika','User \'dhammika\' logged in.','2026-03-24 07:24:35'),
(694,'User Logout','Dhammika','User \'dhammika\' logged out.','2026-03-24 09:32:03'),
(695,'User Login','Sarinda','User \'admin\' logged in.','2026-03-24 09:32:12'),
(696,'Device Edited','Sarinda','Admin updated data for tablet T-1.','2026-03-24 09:48:08'),
(697,'Data Export','Sarinda','Exported full tablet database to CSV.','2026-03-24 09:48:18'),
(698,'User Login','Sarinda','User \'admin\' logged in.','2026-03-24 10:39:44'),
(699,'User Logout','Sarinda','User \'admin\' logged out.','2026-03-24 10:40:21'),
(700,'User Login','Sumith','User \'Sumith\' logged in.','2026-03-24 10:41:04'),
(701,'Filtered Data Export','Sumith','Exported filtered report.','2026-03-24 10:42:28');
/*!40000 ALTER TABLE `system_audit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tablets`
--

DROP TABLE IF EXISTS `tablets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `tablets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device_id` varchar(20) DEFAULT NULL,
  `district` varchar(50) DEFAULT NULL,
  `brand` varchar(50) DEFAULT NULL,
  `serial_number` varchar(100) DEFAULT NULL,
  `asset_no` varchar(50) DEFAULT NULL,
  `imei_number` varchar(50) DEFAULT NULL,
  `charger_status` varchar(50) DEFAULT NULL,
  `cable_status` varchar(50) DEFAULT NULL,
  `simpin_status` varchar(50) DEFAULT NULL,
  `doc_status` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT 'Pending',
  `registered_by` varchar(50) DEFAULT 'Admin',
  `registered_date` timestamp NULL DEFAULT current_timestamp(),
  `model` varchar(100) DEFAULT NULL,
  `inspected_by` varchar(100) DEFAULT NULL,
  `registered_at` timestamp NULL DEFAULT current_timestamp(),
  `inspection_data` text DEFAULT NULL,
  `pouch_status` varchar(50) DEFAULT 'Missing',
  `pen_status` varchar(50) DEFAULT 'Missing',
  `is_deleted` tinyint(1) DEFAULT 0,
  `battery_drain_time` varchar(50) DEFAULT '-',
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_id` (`device_id`),
  UNIQUE KEY `serial_number` (`serial_number`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tablets`
--

LOCK TABLES `tablets` WRITE;
/*!40000 ALTER TABLE `tablets` DISABLE KEYS */;
INSERT INTO `tablets` VALUES
(1,NULL,'Badulla','Samsung','IYGJ7899988','10710','887768976432222','Good','Good','Good','Good','Passed','Sarinda','2026-03-24 09:46:50','SM-T295','Sarinda','2026-03-24 09:46:50','{\"display\": \"Pass\", \"touch\": \"Pass\", \"battery\": \"Pass\", \"cameras\": \"Pass\", \"wifi\": \"Pass\", \"bt\": \"Pass\", \"gps\": \"Pass\", \"speaker\": \"Pass\", \"mic\": \"Pass\", \"charging\": \"Pass\", \"p_btn\": \"Pass\", \"sim\": \"Pass\", \"inspector_notes\": \"\"}','Bulk','Bulk',0,'66');
/*!40000 ALTER TABLE `tablets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `name` varchar(100) NOT NULL,
  `role` varchar(20) DEFAULT 'User',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES
(1,'admin','scrypt:32768:8:1$GoIxnC2ONrdiN3ta$51f27aef292c1c1c0e5bd0c8f33bcade9f5ae7a7a4aafc45d226e7a6d4627537d3538264102262682bfbac064ef70a9b60443a2380933bb50981391665359379','Sarinda','Admin'),
(3,'dhammika','scrypt:32768:8:1$AqxrI9OZQ2vgmW7k$58b1f2c1393b74f7deac01d3d83b5d50d3359f7019f3d97ea589e010b6aa570dafd5d1dec4013c5c64c8b5ea09e995385da8ee6a1a43c4a6c3485bbc4fe3f282','Dhammika','Technician'),
(4,'kosala','scrypt:32768:8:1$Hy9r0Rmuv4JucTD2$53222abab5708cbda4dbe37f82539a4feb1d658bf77dd01abd5edba1118385a917ae98b569cbdfce3fe3625f1133089d4638434de04a342f03633b46cc554870','kosala','Technician'),
(5,'laksaman','scrypt:32768:8:1$j98jPOaotShaRTwz$c1dba3cc17df0903973c2f2ef3e6366eb7406f787fb208a30a9672c9ddb7611e641ecbe35dc48f07fdda9d4a2523f2f183c6be21148fdd39ab05aa8637a10174','Laksaman','Technician'),
(6,'susantha','scrypt:32768:8:1$AWFuj8VFomitCYWN$91c4efed7ce3f82139ede7ce4ee2994bcb276a4bf0b37bffaaa4bee2e2b9d2a932871ef7d7450845cec4b9d3d2030f3593ac4f622a2b5cee27fbacc2b530090c','Susantha','Technician'),
(7,'pubudu','scrypt:32768:8:1$CrP7CmBRia64DJ4e$d2d29399a86a3343662e6b183178bcfd9a2c6c70598f7e65ef4d1c500e0eb3079411ed9bc9d22cd24b573950912df9159df1686d737f53f503f2d7860240574e','Pubudu','Technician'),
(8,'sumith','scrypt:32768:8:1$gzNc6xzGvFYkzG6p$f5d983ccf1994870437ab0cc4fd57ed9da39f1e05502f6834069b9be23e2d41ef324950d2bd24cd7212b38be6e773624d39913e4ba522d8d1f7007253b13e764','Sumith','Technician'),
(10,'tempadmin','scrypt:32768:8:1$VCfcxFTmAXcYiWfN$3f6e8a1d8edf06db3b32912d639628bf2297e303cffa6fa04e9d64486632b57dd51d308dedf820518a0c7bbf3f3dc5e78007f1ac425852b6f1b790fb6105b4fd','Tempadmin','Admin');
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

-- Dump completed on 2026-03-24 23:59:01
