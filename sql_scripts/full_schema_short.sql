-- 完整数据库架构SQL语句（短表名和字段名）

-- 1. 用户相关表
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
CREATE TABLE `account_profile` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `user_id` integer NOT NULL UNIQUE,
    `avatar` varchar(100) NULL,
    `bio` text NULL,
    `phone` varchar(15) NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT `account_profile_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. 中药材相关表
-- 中药材表
CREATE TABLE `medicine` (
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
CREATE TABLE `prescription` (
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
CREATE TABLE `dietary` (
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
CREATE TABLE `acupuncture` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `name` varchar(100) NOT NULL UNIQUE,
    `location` text NULL,
    `functions` text NULL,
    `indications` text NULL,
    `method` text NULL,
    `precautions` text NULL,
    `image` varchar(500) NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. 销售相关表
-- 供应信息表
CREATE TABLE `supply` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `user_id` integer NULL,
    `medicine_id` integer NULL,
    `medicine_name` varchar(100) NOT NULL,
    `spec` varchar(200) NULL,
    `quantity` varchar(50) NULL,
    `location` varchar(200) NULL,
    `origin` varchar(200) NULL,
    `invoice_req` varchar(100) NULL,
    `quality_req` varchar(100) NULL,
    `qualification_req` varchar(100) NULL,
    `sample` varchar(50) NULL,
    `payment` varchar(100) NULL,
    `packaging` varchar(100) NULL,
    `contact_phone` varchar(20) NULL,
    `contact_name` varchar(100) NULL,
    `update_time` varchar(50) NULL,
    `price` varchar(50) NULL,
    `min_order` varchar(50) NULL,
    `bozhou_price` varchar(50) NULL,
    `angui_price` varchar(50) NULL,
    `chengdu_price` varchar(50) NULL,
    `yulin_price` varchar(50) NULL,
    `lianqiao_price` varchar(50) NULL,
    `puning_price` varchar(50) NULL,
    `description` text NULL,
    `created_at` datetime NOT NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT `supply_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE,
    CONSTRAINT `supply_medicine_id_fk` FOREIGN KEY (`medicine_id`) REFERENCES `medicine` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 求购信息表
CREATE TABLE `demand` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `user_id` integer NULL,
    `medicine_name` varchar(100) NOT NULL,
    `spec` varchar(200) NULL,
    `quantity` varchar(50) NULL,
    `location` varchar(200) NULL,
    `origin` varchar(200) NULL,
    `price` varchar(50) NULL,
    `contact_name` varchar(100) NULL,
    `contact_phone` varchar(20) NULL,
    `update_time` varchar(50) NULL,
    `description` text NULL,
    `created_at` datetime NOT NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT `demand_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 价格历史表
CREATE TABLE `price_history` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `medicine_name` varchar(100) NOT NULL,
    `spec` varchar(200) NULL,
    `origin` varchar(200) NULL,
    `date` date NOT NULL,
    `bozhou_price` varchar(50) NULL,
    `angui_price` varchar(50) NULL,
    `chengdu_price` varchar(50) NULL,
    `yulin_price` varchar(50) NULL,
    `lianqiao_price` varchar(50) NULL,
    `puning_price` varchar(50) NULL,
    `supply_id` integer NULL,
    `created_at` datetime NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `price_history_uniq` (`medicine_name`, `spec`, `origin`, `date`),
    CONSTRAINT `price_history_supply_id_fk` FOREIGN KEY (`supply_id`) REFERENCES `supply` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. 新闻相关表
-- 新闻表
CREATE TABLE `news` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `title` varchar(200) NOT NULL,
    `content` text NOT NULL,
    `author` varchar(100) NULL,
    `source` varchar(100) NULL,
    `publish_date` datetime NOT NULL,
    `image` varchar(100) NULL,
    `is_published` tinyint(1) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 新闻分类表
CREATE TABLE `news_category` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `name` varchar(50) NOT NULL UNIQUE,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 新闻分类关联表
CREATE TABLE `news_category_rel` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `news_id` integer NOT NULL,
    `category_id` integer NOT NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT `news_category_rel_news_id_fk` FOREIGN KEY (`news_id`) REFERENCES `news` (`id`) ON DELETE CASCADE,
    CONSTRAINT `news_category_rel_category_id_fk` FOREIGN KEY (`category_id`) REFERENCES `news_category` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. 图像识别相关表
-- 识别记录表
CREATE TABLE `recognition_record` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `user_id` integer NULL,
    `image` varchar(100) NOT NULL,
    `result` json NULL,
    `confidence` float NULL,
    `created_at` datetime NOT NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT `recognition_record_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 药材图像库表
CREATE TABLE `medicine_image` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `medicine_id` integer NOT NULL,
    `image` varchar(100) NOT NULL,
    `description` varchar(200) NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT `medicine_image_medicine_id_fk` FOREIGN KEY (`medicine_id`) REFERENCES `medicine` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. 智能问答相关表
-- 问答记录模型
CREATE TABLE `qa_record` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `user_id` integer NULL,
    `question` text NOT NULL,
    `answer` text NULL,
    `created_at` datetime NOT NULL,
    `model_used` varchar(100) NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT `qa_record_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;