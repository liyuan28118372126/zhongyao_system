-- 新闻表
CREATE TABLE `news_news` (
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
CREATE TABLE `news_newscategory` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `news_id` integer NOT NULL,
    `category_id` integer NOT NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT `news_newscategory_news_id_8f7c4c8a_fk_news_news_id` FOREIGN KEY (`news_id`) REFERENCES `news_news` (`id`) ON DELETE CASCADE,
    CONSTRAINT `news_newscategory_category_id_4a9f65c7_fk_news_category_id` FOREIGN KEY (`category_id`) REFERENCES `news_category` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;