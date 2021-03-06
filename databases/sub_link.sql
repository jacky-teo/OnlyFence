
-- Database: `sub_link`
--
CREATE DATABASE IF NOT EXISTS SUB_LINK;
USE SUB_LINK;


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
	TELEGRAM varchar(64) NOT NULL,
	CREATED timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	MODIFIED timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (CREATORID, CONSUMERID)
) ENGINE=InnoDB;

INSERT INTO SUBSCRIPTION_LINK(CREATORID,CONSUMERID, TELEGRAM, CREATED,MODIFIED) 
VALUES 
('CR001', 'CON001', '@jackyteojianqi','2020-06-12 02:14:55', '2020-06-12 02:14:55' ),
('CR002', 'CON002', '@erlynnehazey', '2020-06-12 02:14:55', '2020-06-12 02:14:55');