-- 中药材表
CREATE TABLE `medicine_medicine` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `name` varchar(100) NOT NULL UNIQUE,
    `latin_name` varchar(200) NULL,
    `category` varchar(50) NULL,
    `origin` varchar(100) NULL,
    `properties` text NULL,
    `functions` text NULL,
    `indications` text NULL,
    `usage` text NULL,
    `precautions` text NULL,
    `image` varchar(500) NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 方剂表
CREATE TABLE `medicine_prescription` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `name` varchar(100) NOT NULL UNIQUE,
    `ingredients` text NOT NULL,
    `dosage` text NULL,
    `preparation` text NULL,
    `functions` text NULL,
    `indications` text NULL,
    `precautions` text NULL,
    `image` varchar(500) NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 药膳食疗表
CREATE TABLE `medicine_dietarytherapy` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `name` varchar(100) NOT NULL UNIQUE,
    `ingredients` text NOT NULL,
    `preparation` text NULL,
    `functions` text NULL,
    `indications` text NULL,
    `precautions` text NULL,
    `image` varchar(500) NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 针灸穴位表
CREATE TABLE `medicine_acupuncturepoint` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `name` varchar(100) NOT NULL UNIQUE,
    `location` text NULL,
    `functions` text NULL,
    `indications` text NULL,
    `acupuncture_method` text NULL,
    `precautions` text NULL,
    `image` varchar(500) NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;