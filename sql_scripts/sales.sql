-- 供应信息表
CREATE TABLE `sales_supply` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `user_id` integer NULL,
    `medicine_id` integer NULL,
    `medicine_name` varchar(100) NOT NULL,
    `specification` varchar(200) NULL,
    `quantity` varchar(50) NULL,
    `location` varchar(200) NULL,
    `origin` varchar(200) NULL,
    `invoice_requirement` varchar(100) NULL,
    `quality_requirement` varchar(100) NULL,
    `qualification_requirement` varchar(100) NULL,
    `sample` varchar(50) NULL,
    `payment` varchar(100) NULL,
    `packaging` varchar(100) NULL,
    `contact_phone` varchar(20) NULL,
    `contact_name` varchar(100) NULL,
    `update_time` varchar(50) NULL,
    `price` varchar(50) NULL,
    `minimum_order` varchar(50) NULL,
    `bozhou_price` varchar(50) NULL,
    `angui_price` varchar(50) NULL,
    `chengdu_price` varchar(50) NULL,
    `yulin_price` varchar(50) NULL,
    `lianqiao_price` varchar(50) NULL,
    `puning_price` varchar(50) NULL,
    `description` text NULL,
    `created_at` datetime NOT NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT `sales_supply_user_id_136a234f_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE,
    CONSTRAINT `sales_supply_medicine_id_6f063a08_fk_medicine_medicine_id` FOREIGN KEY (`medicine_id`) REFERENCES `medicine_medicine` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 求购信息表
CREATE TABLE `sales_demand` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `user_id` integer NULL,
    `medicine_name` varchar(100) NOT NULL,
    `specification` varchar(200) NULL,
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
    CONSTRAINT `sales_demand_user_id_891263d3_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 价格历史表
CREATE TABLE `sales_pricehistory` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `medicine_name` varchar(100) NOT NULL,
    `specification` varchar(200) NULL,
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
    UNIQUE KEY `sales_pricehistory_medicine_name_specification_origin_date_28e4113e_uniq` (`medicine_name`, `specification`, `origin`, `date`),
    CONSTRAINT `sales_pricehistory_supply_id_1a3d4134_fk_sales_supply_id` FOREIGN KEY (`supply_id`) REFERENCES `sales_supply` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;