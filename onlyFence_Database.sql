-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 11, 2022 at 11:12 PM
-- Server version: 5.7.19
-- PHP Version: 7.1.9

--
-- Database: `OnlyFence`
--
CREATE DATABASE IF NOT EXISTS ONLYFENCE;
USE ONLYFENCE;

-- ---------------------------------------------------------------- --
--                     CREATOR ACCOUNT TABLE                        --
-- ---------------------------------------------------------------- --

--
-- Table structure for table `CREATORACCOUNT_SEQ` --
--
DROP TABLE IF EXISTS CREATORACCOUNT_SEQ;
CREATE TABLE CREATORACCOUNT_SEQ
(
	CREATORID INT NOT NULL AUTO_INCREMENT PRIMARY KEY
);

--
-- Table structure for table `CREATORACCOUNT` --
--
DROP TABLE IF EXISTS CREATORACCOUNT;

CREATE TABLE IF NOT EXISTS CREATORACCOUNT (
	CREATORID varchar(64) NOT NULL,
	USERNAME varchar(64) NOT NULL,
	PASSWORD varchar(64) NOT NULL,
	EMAIL varchar(64) NOT NULL,
    PAYPALID varchar(64) NOT NULL,
	PRICE decimal(10,2) NOT NULL,
	PRIMARY KEY (CREATORID)
) ENGINE=InnoDB;

--
-- Trigger for autoincrement for `CREATORACCOUNT` --
--

DELIMITER $$
CREATE TRIGGER tg_creatoraccount_insert
BEFORE INSERT ON CREATORACCOUNT
FOR EACH ROW
BEGIN
	INSERT INTO CREATORACCOUNT_SEQ VALUES (NULL);
	SET NEW.CREATORID = CONCAT('CR', LPAD(LAST_INSERT_ID(), 3, '0'));
END$$
DELIMITER ;

--
-- Insert Data into `CREATORACCOUNT` --
--
INSERT INTO CREATORACCOUNT(USERNAME,PASSWORD,EMAIL,PRICE) 
VALUES 
('jackyteo', 'pass123', 'jacky.teo.2020@smu.edu.sg',100.00),
('notJacky', 'pass123', 'jackyteojianqi@gmail.com',233.50);

-- ---------------------------------------------------------------- --
--                     CONSUMER ACCOUNT TABLE                       --
-- ---------------------------------------------------------------- --

--
-- Table structure for table `CONSUMERACCOUNT_SEQ`
--
DROP TABLE IF EXISTS CONSUMERACCOUNT_SEQ;

CREATE TABLE CONSUMERACCOUNT_SEQ
(
	CONSUMERID INT NOT NULL AUTO_INCREMENT PRIMARY KEY
);

--
-- Table structure for table `CONSUMERACCOUNT` --
--
DROP TABLE IF EXISTS CONSUMERACCOUNT;

CREATE TABLE IF NOT EXISTS CONSUMERACCOUNT (
	CONSUMERID varchar(64) NOT NULL,
	USERNAME varchar(64) NOT NULL,
	PASSWORD varchar(64) NOT NULL,
	TELEGRAM varchar(64) NOT NULL,
	PRIMARY KEY (CONSUMERID)
) ENGINE=InnoDB;

--
-- Trigger for autoincrement for `CREATORACCOUNT`
--

DELIMITER $$
CREATE TRIGGER tg_consumeraccount_insert
BEFORE INSERT ON CONSUMERACCOUNT
FOR EACH ROW
BEGIN
	INSERT INTO CONSUMERACCOUNT_SEQ VALUES (NULL);
	SET NEW.CONSUMERID = CONCAT('CON', LPAD(LAST_INSERT_ID(), 3, '0'));
END$$
DELIMITER ;

--
-- Insert Data into CONSUMERACCOUNT -- 
--

INSERT INTO CONSUMERACCOUNT(USERNAME,PASSWORD,TELEGRAM) 
VALUES ('imnew', 'pass123','@tinklebell'),
('logi', 'pass123','@hutthutt');

-- ---------------------------------------------------------------- --
--                     SUBSCRIPTION_LINK TABLE                        --
-- ---------------------------------------------------------------- --

--
-- Table structure for table `SUBSCRIPTION LINK` --
--
DROP TABLE IF EXISTS SUBSCRIPTION_LINK;
CREATE TABLE SUBSCRIPTION_LINK(
	CREATORID varchar(64) NOT NULL,
	CONSUMERID varchar(64) NOT NULL,
	CREATED timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	MODIFIED timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (CREATORID, CONSUMERID),
	CONSTRAINT FK_SUBSCRIBED_CREATORID FOREIGN KEY (CREATORID) REFERENCES CREATORACCOUNT(CREATORID),
	CONSTRAINT FK_SUBSCRIBED_CONSUMERID FOREIGN KEY (CONSUMERID) REFERENCES CONSUMERACCOUNT(CONSUMERID)
) ENGINE=InnoDB;

INSERT INTO SUBSCRIPTION_LINK(CREATORID,CONSUMERID,CREATED,MODIFIED) 
VALUES 
('CR001', 'CON001','2020-06-12 02:14:55', '2020-06-12 02:14:55' ),
('CR002', 'CON002', '2020-06-12 02:14:55', '2020-06-12 02:14:55');


-- ---------------------------------------------------------------- --
--                     CREATOR_CONTENT TABLE                        --
-- ---------------------------------------------------------------- --

--
-- Table structure for table `CREATOR_CONTENT_SEQ` --
--
DROP TABLE IF EXISTS CREATOR_CONTENT_SEQ;
CREATE TABLE CREATOR_CONTENT_SEQ
(
	POSTID INT NOT NULL AUTO_INCREMENT PRIMARY KEY
);

--
-- Table structure for table `CREATOR_CONTENT` --
--

DROP TABLE IF EXISTS CREATOR_CONTENT;
CREATE TABLE CREATOR_CONTENT(
	POSTID varchar(64) NOT NULL,
	CREATORID varchar(64) NOT NULL,
	DESCRIPTION varchar(64) NOT NULL,
	IMAGE_ID varchar(64) NOT NULL,
	POST_DATE timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	MODIFIED timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (POSTID, CREATORID),
	CONSTRAINT FK_CREATORID FOREIGN KEY (CREATORID) REFERENCES CREATORACCOUNT(CREATORID)
) ENGINE=InnoDB;

--
-- Trigger for autoincrement for `CREATOR_CONTENT`
--

DELIMITER $$
CREATE TRIGGER tg_creator_content_insert
BEFORE INSERT ON CREATOR_CONTENT
FOR EACH ROW
BEGIN
	INSERT INTO CREATOR_CONTENT_SEQ VALUES (NULL);
	SET NEW.POSTID = CONCAT('P', LPAD(LAST_INSERT_ID(), 3, '0'));
END$$
DELIMITER ;

INSERT INTO CREATOR_CONTENT(CREATORID,DESCRIPTION,IMAGE_ID) 
VALUES 
('CR001', 'this is img1', "img1"),
('CR001', 'this is img2', "img2"),
('CR001', 'this is img3', "img3"),
('CR001', 'this is img4', "img4"),
('CR002', 'this is cr2img1', 'cr2img1'),
('CR002', 'this is cr2img2', 'cr2img2'),
('CR002', 'this is cr2img3', 'cr2img3');


-- ---------------------------------------------------------------- --
--                     PAYMENT_LOG TABLE                        --
-- ---------------------------------------------------------------- --

--
-- Table structure for table `PAYMENT_LOG` --
--

DROP TABLE IF EXISTS PAYMENT_LOG;
CREATE TABLE PAYMENT_LOG(
	TRANSACTIONID varchar(64) NOT NULL,
	CONSUMERID varchar(64) NOT NULL,
    CREATORID varchar(64) NOT NULL,
	PAYMENT_AMOUNT decimal(10,2) NOT NULL,
	TRANSACTION_DATE timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	MODIFIED timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (TRANSACTIONID),
	CONSTRAINT FK_PAYMENT_CREATORID FOREIGN KEY (CREATORID) REFERENCES CREATORACCOUNT(CREATORID),
    CONSTRAINT FK_PAYMENT_CONSUMERID FOREIGN KEY (CONSUMERID) REFERENCES CONSUMERACCOUNT(CONSUMERID)
) ENGINE=InnoDB;


-- ---------------------------------------------------------------- --
--                     NOTIFICATION TABLE                        --
-- ---------------------------------------------------------------- --
DROP TABLE IF EXISTS NOTIFICATION;
CREATE TABLE NOTIFICATION(
	CHATID varchar(64) NOT NULL,
	CONSUMERID varchar(64) NOT NULL,
    TELEGRAMTAG varchar(64) NOT NULL,
	PRIMARY KEY (CHATID),
	CONSTRAINT FK_NOTIFICATION_CONSUMERID FOREIGN KEY (CONSUMERID) REFERENCES CONSUMERACCOUNT(CONSUMERID)
) ENGINE=InnoDB;
