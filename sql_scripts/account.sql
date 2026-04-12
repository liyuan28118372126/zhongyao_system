-- Django默认的用户表
CREATE TABLE `auth_user` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `password` varchar(128) NOT NULL,
    `last_login` datetime NULL,
    `is_superuser` tinyint(1) NOT NULL,
    `username` varchar(150) NOT NULL UNIQUE,
    `first_name` varchar(30) NOT NULL,
    `last_name` varchar(150) NOT NULL,
    `email` varchar(254) NOT NULL,
    `is_staff` tinyint(1) NOT NULL,
    `is_active` tinyint(1) NOT NULL,
    `date_joined` datetime NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 用户资料表
CREATE TABLE `account_userprofile` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `user_id` integer NOT NULL UNIQUE,
    `avatar` varchar(100) NULL,
    `bio` text NULL,
    `phone_number` varchar(15) NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT `account_userprofile_user_id_868e82f3_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;