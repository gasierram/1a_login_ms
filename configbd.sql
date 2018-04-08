CREATE DATABASE IF NOT EXISTS users;

CREATE TABLE `users`.`tbl_user` (
  `user_id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_name` VARCHAR(255) NULL,
  `user_email` VARCHAR(255) NULL,
  `user_password` VARCHAR(255) NULL,
  PRIMARY KEY (`user_id`));


USE `users`;
DROP procedure IF EXISTS `sp_createUser`;
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
    IN p_name VARCHAR(255),
    IN p_email VARCHAR(255),
    IN p_password VARCHAR(255)
)
BEGIN
    if ( select exists (select 1 from tbl_user where user_email = p_email) ) THEN
     
        select 'Email Exists !!';
     
    ELSE
     
        insert into tbl_user
        (
            user_name,
            user_email,
            user_password
        )
        values
        (
            p_name,
            p_email,
            p_password
        );
     
    END IF;
END$$
DELIMITER ;


USE `users`;
DROP procedure IF EXISTS `sp_AuthenticateUser`;

DELIMITER $$
USE `users`$$
CREATE PROCEDURE `sp_AuthenticateUser` (
IN p_email VARCHAR(255)
)
BEGIN

     select * from tbl_user where user_email = p_email;

END$$

DELIMITER ;



USE `users`;
DROP procedure IF EXISTS `sp_GetAllItems`;

DELIMITER $$
USE `users`$$
CREATE PROCEDURE `sp_GetAllItems` (
)
BEGIN
    select * from tbl_user; 
END$$

DELIMITER ;

USE `users`;
DROP procedure IF EXISTS `sp_deleteUser`;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_deleteUser`(
    IN p_email VARCHAR(255)
)
BEGIN
	DELETE FROM tbl_user where user_email = p_email;
END$$
DELIMITER ;
