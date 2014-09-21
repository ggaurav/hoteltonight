create database restauranttonight;

use restauranttonight;

CREATE TABLE `restaurants` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`jd_id` int(11) DEFAULT NULL,
	`name` varchar(255) CHARACTER NOT NULL,
	`latitude` decimal(12,7) DEFAULT NULL,
	`longitude` decimal(12,7) DEFAULT NULL,
	`city_id` int(11) DEFAULT NULL,
	`address` varchar(255) CHARACTER,
	`cost_for_2` int(11),
	`email` varchar(150) NOT NULL DEFAULT '',
	`phone` int(15) DEFAULT NULL,
	PRIMARY KEY (`id`),
	KEY `lat` (`latitude`),
	KEY `lng` (`longitude`),
	KEY `r_name_idx1` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `users` (
	`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
	`name` varchar(50) DEFAULT NULL,
	`email` varchar(150) NOT NULL DEFAULT '',
	`device_token` varchar(64) NOT NULL,
	PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


CREATE TABLE `deals` (
	`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
	`text` varchar(50) DEFAULT NULL,
	`start_time` varchar(5000) DEFAULT NULL,	
	`end_time` varchar(5000) DEFAULT NULL,
	`date` date DEFAULT NULL,		
	`status` enum('new','published','closed') DEFAULT 'new',
	`reservations_allowed` int(11),
	PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


CREATE TABLE `user_deals` (
	`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
	`user_id` int(11) DEFAULT NULL,
	`deal_id` int(11) DEFAULT NULL,
	`status` enum('reserved','claimed','expired') DEFAULT 'reserved',
	PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `restaurant_owners` (
	`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
	`name` varchar(255) CHARACTER NOT NULL,
	`password` varchar(255) CHARACTER NOT NULL,	
	PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

