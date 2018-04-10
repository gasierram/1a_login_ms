CREATE DATABASE IF NOT EXISTS users;

-- ----------------------------
-- Table structure for user
    -- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
    `id` int(50) NOT NULL AUTO_INCREMENT,
    `username` varchar(255) DEFAULT NULL,
    `email` varchar(255) NOT NULL UNIQUE,
    `password` varchar(255) NOT  NULL,
    PRIMARY KEY (`id`) 
) ;

DROP TABLE IF EXISTS `usersapp`;
CREATE TABLE `usersapp`  (
    `id` int(50) NOT NULL AUTO_INCREMENT,
    `name` varchar(255) DEFAULT NULL,
    `lastname` varchar(255) DEFAULT NULL ,
    `id_code` int NOt NULL UNIQUE,
    `email` varchar(255) DEFAULT NULL ,
    `id_type` varchar(255) DEFAULT NULL,
    PRIMARY KEY (`id`) 
) ;