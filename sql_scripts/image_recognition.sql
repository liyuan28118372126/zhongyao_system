-- 识别记录表
CREATE TABLE `image_recognition_recognitionrecord` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `user_id` integer NULL,
    `image` varchar(100) NOT NULL,
    `result` json NULL,
    `confidence` float NULL,
    `created_at` datetime NOT NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT `image_recognition_recognitionrecord_user_id_3a5e7c72_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 药材图像库表
CREATE TABLE `image_recognition_medicineimage` (
    `id` integer NOT NULL AUTO_INCREMENT,
    `medicine_id` integer NOT NULL,
    `image` varchar(100) NOT NULL,
    `description` varchar(200) NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT `image_recognition_medicineimage_medicine_id_4c8d4e24_fk_medicine_medicine_id` FOREIGN KEY (`medicine_id`) REFERENCES `medicine_medicine` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;