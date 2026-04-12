-- 完整数据库架构SQL语句（短表名和字段名）
-- 包含默认值和字段说明

-- 1. 用户相关表
-- Django默认的用户表
CREATE TABLE `auth_user` (
    `id` integer NOT NULL AUTO_INCREMENT COMMENT '用户ID',
    `password` varchar(128) NOT NULL COMMENT '密码哈希',
    `last_login` datetime NULL COMMENT '最后登录时间',
    `is_superuser` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否超级用户',
    `username` varchar(150) NOT NULL UNIQUE COMMENT '用户名',
    `first_name` varchar(30) NOT NULL DEFAULT '' COMMENT '名',
    `last_name` varchar(150) NOT NULL DEFAULT '' COMMENT '姓',
    `email` varchar(254) NOT NULL DEFAULT '' COMMENT '邮箱',
    `is_staff` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否管理员',
    `is_active` tinyint(1) NOT NULL DEFAULT 1 COMMENT '是否激活',
    `date_joined` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '加入时间',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 用户资料表
CREATE TABLE `account_profile` (
    `id` integer NOT NULL AUTO_INCREMENT COMMENT '资料ID',
    `user_id` integer NOT NULL UNIQUE COMMENT '用户ID',
    `avatar` varchar(100) NULL DEFAULT NULL COMMENT '头像路径',
    `bio` text NULL DEFAULT NULL COMMENT '个人简介',
    `phone` varchar(15) NULL DEFAULT NULL COMMENT '联系电话',
    PRIMARY KEY (`id`),
    CONSTRAINT `account_profile_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户资料表';

-- 2. 中药材相关表
-- 中药材表
CREATE TABLE `medicine` (
    `id` integer NOT NULL AUTO_INCREMENT COMMENT '药材ID',
    `name` varchar(100) NOT NULL UNIQUE COMMENT '药材名称',
    `latin_name` varchar(200) NULL DEFAULT NULL COMMENT '拉丁名',
    `category` varchar(50) NULL DEFAULT NULL COMMENT '分类',
    `origin` varchar(100) NULL DEFAULT NULL COMMENT '产地',
    `properties` text NULL DEFAULT NULL COMMENT '性味归经',
    `functions` text NULL DEFAULT NULL COMMENT '功效',
    `indications` text NULL DEFAULT NULL COMMENT '主治',
    `usage` text NULL DEFAULT NULL COMMENT '用法用量',
    `precautions` text NULL DEFAULT NULL COMMENT '注意事项',
    `image` varchar(500) NULL DEFAULT NULL COMMENT '图片URL',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='中药材表';

-- 方剂表
CREATE TABLE `prescription` (
    `id` integer NOT NULL AUTO_INCREMENT COMMENT '方剂ID',
    `name` varchar(100) NOT NULL UNIQUE COMMENT '方剂名称',
    `ingredients` text NOT NULL COMMENT '组成',
    `dosage` text NULL DEFAULT NULL COMMENT '用量',
    `preparation` text NULL DEFAULT NULL COMMENT '制法',
    `functions` text NULL DEFAULT NULL COMMENT '功效',
    `indications` text NULL DEFAULT NULL COMMENT '主治',
    `precautions` text NULL DEFAULT NULL COMMENT '注意事项',
    `image` varchar(500) NULL DEFAULT NULL COMMENT '图片URL',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='方剂表';

-- 药膳食疗表
CREATE TABLE `dietary` (
    `id` integer NOT NULL AUTO_INCREMENT COMMENT '药膳ID',
    `name` varchar(100) NOT NULL UNIQUE COMMENT '药膳名称',
    `ingredients` text NOT NULL COMMENT '原料',
    `preparation` text NULL DEFAULT NULL COMMENT '制法',
    `functions` text NULL DEFAULT NULL COMMENT '功效',
    `indications` text NULL DEFAULT NULL COMMENT '适用症',
    `precautions` text NULL DEFAULT NULL COMMENT '注意事项',
    `image` varchar(500) NULL DEFAULT NULL COMMENT '图片URL',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='药膳食疗表';

-- 针灸穴位表
CREATE TABLE `acupuncture` (
    `id` integer NOT NULL AUTO_INCREMENT COMMENT '穴位ID',
    `name` varchar(100) NOT NULL UNIQUE COMMENT '穴位名称',
    `location` text NULL DEFAULT NULL COMMENT '定位',
    `functions` text NULL DEFAULT NULL COMMENT '功效',
    `indications` text NULL DEFAULT NULL COMMENT '主治',
    `method` text NULL DEFAULT NULL COMMENT '刺灸法',
    `precautions` text NULL DEFAULT NULL COMMENT '注意事项',
    `image` varchar(500) NULL DEFAULT NULL COMMENT '图片URL',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='针灸穴位表';

-- 3. 销售相关表
-- 供应信息表
CREATE TABLE `supply` (
    `id` integer NOT NULL AUTO_INCREMENT COMMENT '供应ID',
    `user_id` integer NULL DEFAULT NULL COMMENT '用户ID',
    `medicine_id` integer NULL DEFAULT NULL COMMENT '药材ID',
    `medicine_name` varchar(100) NOT NULL COMMENT '药材名称',
    `spec` varchar(200) NULL DEFAULT NULL COMMENT '规格',
    `quantity` varchar(50) NULL DEFAULT NULL COMMENT '供应数量',
    `location` varchar(200) NULL DEFAULT NULL COMMENT '药材库存',
    `origin` varchar(200) NULL DEFAULT NULL COMMENT '药材产地',
    `invoice_req` varchar(100) NULL DEFAULT NULL COMMENT '票据需求',
    `quality_req` varchar(100) NULL DEFAULT NULL COMMENT '质量需求',
    `qualification_req` varchar(100) NULL DEFAULT NULL COMMENT '资质要求',
    `sample` varchar(50) NULL DEFAULT NULL COMMENT '寄样',
    `payment` varchar(100) NULL DEFAULT NULL COMMENT '付款方式',
    `packaging` varchar(100) NULL DEFAULT NULL COMMENT '包装',
    `contact_phone` varchar(20) NULL DEFAULT NULL COMMENT '联系电话',
    `contact_name` varchar(100) NULL DEFAULT NULL COMMENT '联系人',
    `update_time` varchar(50) NULL DEFAULT NULL COMMENT '更新时间',
    `price` varchar(50) NULL DEFAULT NULL COMMENT '售价',
    `min_order` varchar(50) NULL DEFAULT NULL COMMENT '起售量',
    `bozhou_price` varchar(50) NULL DEFAULT NULL COMMENT '亳州价格',
    `angui_price` varchar(50) NULL DEFAULT NULL COMMENT '安国价格',
    `chengdu_price` varchar(50) NULL DEFAULT NULL COMMENT '成都价格',
    `yulin_price` varchar(50) NULL DEFAULT NULL COMMENT '玉林价格',
    `lianqiao_price` varchar(50) NULL DEFAULT NULL COMMENT '廉桥价格',
    `puning_price` varchar(50) NULL DEFAULT NULL COMMENT '普宁价格',
    `description` text NULL DEFAULT NULL COMMENT '描述',
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`),
    CONSTRAINT `supply_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE,
    CONSTRAINT `supply_medicine_id_fk` FOREIGN KEY (`medicine_id`) REFERENCES `medicine` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='供应信息表';

-- 求购信息表
CREATE TABLE `demand` (
    `id` integer NOT NULL AUTO_INCREMENT COMMENT '求购ID',
    `user_id` integer NULL DEFAULT NULL COMMENT '用户ID',
    `medicine_name` varchar(100) NOT NULL COMMENT '药材名称',
    `spec` varchar(200) NULL DEFAULT NULL COMMENT '规格',
    `quantity` varchar(50) NULL DEFAULT NULL COMMENT '求购数量',
    `location` varchar(200) NULL DEFAULT NULL COMMENT '地区',
    `origin` varchar(200) NULL DEFAULT NULL COMMENT '产地要求',
    `price` varchar(50) NULL DEFAULT NULL COMMENT '价格',
    `contact_name` varchar(100) NULL DEFAULT NULL COMMENT '联系人',
    `contact_phone` varchar(20) NULL DEFAULT NULL COMMENT '联系电话',
    `update_time` varchar(50) NULL DEFAULT NULL COMMENT '更新时间',
    `description` text NULL DEFAULT NULL COMMENT '描述',
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`),
    CONSTRAINT `demand_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='求购信息表';

-- 价格历史表
CREATE TABLE `price_history` (
    `id` integer NOT NULL AUTO_INCREMENT COMMENT '价格历史ID',
    `medicine_name` varchar(100) NOT NULL COMMENT '药材名称',
    `spec` varchar(200) NULL DEFAULT NULL COMMENT '规格',
    `origin` varchar(200) NULL DEFAULT NULL COMMENT '产地',
    `date` date NOT NULL COMMENT '日期',
    `bozhou_price` varchar(50) NULL DEFAULT NULL COMMENT '亳州价格',
    `angui_price` varchar(50) NULL DEFAULT NULL COMMENT '安国价格',
    `chengdu_price` varchar(50) NULL DEFAULT NULL COMMENT '成都价格',
    `yulin_price` varchar(50) NULL DEFAULT NULL COMMENT '玉林价格',
    `lianqiao_price` varchar(50) NULL DEFAULT NULL COMMENT '廉桥价格',
    `puning_price` varchar(50) NULL DEFAULT NULL COMMENT '普宁价格',
    `supply_id` integer NULL DEFAULT NULL COMMENT '供应信息ID',
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `price_history_uniq` (`medicine_name`, `spec`, `origin`, `date`),
    CONSTRAINT `price_history_supply_id_fk` FOREIGN KEY (`supply_id`) REFERENCES `supply` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='价格历史表';

-- 4. 新闻相关表
-- 新闻表
CREATE TABLE `news` (
    `id` integer NOT NULL AUTO_INCREMENT COMMENT '新闻ID',
    `title` varchar(200) NOT NULL COMMENT '标题',
    `content` text NOT NULL COMMENT '内容',
    `author` varchar(100) NULL DEFAULT NULL COMMENT '作者',
    `source` varchar(100) NULL DEFAULT NULL COMMENT '来源',
    `publish_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '发布日期',
    `image` varchar(100) NULL DEFAULT NULL COMMENT '图片路径',
    `is_published` tinyint(1) NOT NULL DEFAULT 1 COMMENT '是否发布',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='新闻表';

-- 新闻分类表
CREATE TABLE `news_category` (
    `id` integer NOT NULL AUTO_INCREMENT COMMENT '分类ID',
    `name` varchar(50) NOT NULL UNIQUE COMMENT '分类名称',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='新闻分类表';

-- 新闻分类关联表
CREATE TABLE `news_category_rel` (
    `id` integer NOT NULL AUTO_INCREMENT COMMENT '关联ID',
    `news_id` integer NOT NULL COMMENT '新闻ID',
    `category_id` integer NOT NULL COMMENT '分类ID',
    PRIMARY KEY (`id`),
    CONSTRAINT `news_category_rel_news_id_fk` FOREIGN KEY (`news_id`) REFERENCES `news` (`id`) ON DELETE CASCADE,
    CONSTRAINT `news_category_rel_category_id_fk` FOREIGN KEY (`category_id`) REFERENCES `news_category` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='新闻分类关联表';

-- 5. 图像识别相关表
-- 识别记录表
CREATE TABLE `recognition_record` (
    `id` integer NOT NULL AUTO_INCREMENT COMMENT '记录ID',
    `user_id` integer NULL DEFAULT NULL COMMENT '用户ID',
    `image` varchar(100) NOT NULL COMMENT '图像路径',
    `result` json NULL DEFAULT NULL COMMENT '识别结果',
    `confidence` float NULL DEFAULT NULL COMMENT '置信度',
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`),
    CONSTRAINT `recognition_record_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='识别记录表';

-- 药材图像库表
CREATE TABLE `medicine_image` (
    `id` integer NOT NULL AUTO_INCREMENT COMMENT '图像ID',
    `medicine_id` integer NOT NULL COMMENT '药材ID',
    `image` varchar(100) NOT NULL COMMENT '图像路径',
    `description` varchar(200) NULL DEFAULT NULL COMMENT '描述',
    PRIMARY KEY (`id`),
    CONSTRAINT `medicine_image_medicine_id_fk` FOREIGN KEY (`medicine_id`) REFERENCES `medicine` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='药材图像库表';

-- 6. 智能问答相关表
-- 问答记录模型
CREATE TABLE `qa_record` (
    `id` integer NOT NULL AUTO_INCREMENT COMMENT '记录ID',
    `user_id` integer NULL DEFAULT NULL COMMENT '用户ID',
    `question` text NOT NULL COMMENT '问题',
    `answer` text NULL DEFAULT NULL COMMENT '回答',
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `model_used` varchar(100) NULL DEFAULT NULL COMMENT '使用模型',
    PRIMARY KEY (`id`),
    CONSTRAINT `qa_record_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='问答记录表';