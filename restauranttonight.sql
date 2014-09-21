create database restauranttonight;

use restauranttonight;

CREATE TABLE `locality` (
	`id` int(11) NOT NULL AUTO_INCREMENT,	
	`name` varchar(255) NOT NULL,
	`latitude` decimal(12,7) NOT NULL,
	`longitude` decimal(12,7) NOT NULL,
	`city_id` int(11) DEFAULT NULL,
	PRIMARY KEY (`id`),
	KEY `lat` (`latitude`),
	KEY `lng` (`longitude`)	
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `restaurants` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`jd_id` int(11) NOT NULL,
	`jd_doc_id` int(11) NOT NULL,	
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`jd_id` int(11) NOT NULL,
	`name` varchar(255) NOT NULL,
	`latitude` decimal(12,7) NOT NULL,
	`longitude` decimal(12,7) NOT NULL,
	`city_id` int(11) DEFAULT NULL,
	`address` varchar(255) DEFAULT NULL,
	`cost_for_2` int(11) DEFAULT NULL,
	`email` varchar(150) DEFAULT NULL,
	`phone` int(15) DEFAULT NULL,
	`pic_url` varchar(200) DEFAULT NULL,
	`jd_doc_id` varchar(50) NOT NULL,
	`owner_id` int(11) NOT NULL,
	PRIMARY KEY (`id`),
	KEY `lat` (`latitude`),
	KEY `lng` (`longitude`),
	KEY `r_name_idx1` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `users` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `device_token` varchar(64) NOT NULL,
  `phone` varchar(50) NOT NULL,
  `card_id` varchar(150) NOT NULL,
  `customer_id` varchar(150) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8

CREATE TABLE `deals` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `text` varchar(5000) DEFAULT NULL,
  `start_time` varchar(50) DEFAULT NULL,
  `end_time` varchar(50) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `status` enum('new','published','closed') DEFAULT 'new',
  `reservations_allowed` int(11) DEFAULT NULL,
  `restaurant_id` int(11) DEFAULT NULL,
  `deal_type` enum('percent','absolute','free_text') DEFAULT 'absolute',
  `deal_msg` varchar(5000) DEFAULT NULL,
  PRIMARY KEY (`id`),
  	KEY `restaurant_id` (`date`),
	KEY `date` (`date`),
	KEY `start_time` (`start_time`),
	KEY `end_time` (`end_time`)
) ENGINE=InnoDB AUTO_INCREMENT=1DEFAULT CHARSET=utf8;


CREATE TABLE `user_deals` (
	`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
	`user_id` int(11) DEFAULT NULL,
	`deal_id` int(11) DEFAULT NULL,
	`status` enum('reserved','claimed','expired') DEFAULT 'reserved',	
	PRIMARY KEY (`id`),
	UNIQUE KEY `uid_did` (`user_id`,`deal_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `restaurant_owners` (
	`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
	`password` varchar(255) NOT NULL,
	`email` varchar(255) NOT NULL,		
	PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

