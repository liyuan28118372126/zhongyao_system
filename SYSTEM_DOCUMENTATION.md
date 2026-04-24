# 中药系统 - 完整说明文档

## 一、项目概述

### 1.1 项目简介

中药系统（Zhongyao System）是一个基于 Python+Django 开发的融合大模型的综合性中药信息平台，旨在为用户提供中药材相关的全方位服务。系统集成了中药图像识别、药材资料管理、销售、价格查询、药闻资讯和大模型答疑等核心功能，为中药材从业者、研究者和爱好者提供便捷的信息获取和交互平台。

### 1.2 项目定位

- **面向用户**：中药材从业者、研究者、爱好者
- **核心价值**：提供全面、准确、便捷的中药材信息服务
- **技术特色**：融合大模型智能问答与图像识别技术

### 1.3 版本信息

- **系统版本**：V2.0
- **最后更新**：2026年4月
- **开发框架**：Django 4.2+
- **Python版本**：Python 3.12+

---

## 二、系统功能模块

### 2.1 用户管理模块（account）

**功能描述**：提供用户注册、登录、个人信息管理等基础功能。

**核心功能**：
- 用户注册与登录
- 个人资料编辑（头像、简介、联系电话）
- 密码修改
- 权限管理（普通用户/管理员）

**相关文件**：
```
apps/account/
├── models.py          # 用户模型定义
├── views.py           # 视图函数
├── forms.py           # 表单验证
├── urls.py            # URL路由
├── admin.py           # 后台管理配置
├── apps.py            # 应用配置
└── templates/account/
    ├── login.html     # 登录页面
    ├── signup.html    # 注册页面
    ├── profile.html   # 个人中心
    └── edit_profile.html  # 编辑资料页面
```

**数据表**：
- `auth_user` - Django用户表
- `account_profile` - 用户资料表

---

### 2.2 中药材资料模块（medicine）

**功能描述**：提供中药材、方剂、药膳食疗、针灸穴位等资料的查询和管理。

**核心功能**：
- 中药材信息浏览与搜索
- 方剂管理
- 药膳食疗配方
- 针灸穴位信息
- 多条件搜索筛选

**相关文件**：
```
apps/medicine/
├── models.py           # 数据模型
├── views.py            # 视图函数
├── urls.py             # URL路由
├── admin.py            # 后台管理
├── apps.py             # 应用配置
└── templates/medicine/
    ├── index.html              # 首页
    ├── medicine_list.html      # 药材列表
    ├── medicine_detail.html    # 药材详情
    ├── prescription_list.html  # 方剂列表
    ├── prescription_detail.html # 方剂详情
    ├── dietary_therapy_list.html    # 药膳列表
    ├── dietary_therapy_detail.html  # 药膳详情
    ├── acupuncture_point_list.html  # 穴位列表
    ├── acupuncture_point_detail.html # 穴位详情
    └── search_results.html     # 搜索结果
```

**数据表**：
- `medicine` - 中药材表
- `prescription` - 方剂表
- `dietary` - 药膳食疗表
- `acupuncture` - 针灸穴位表

---

### 2.3 图像识别模块（image_recognition）

**功能描述**：基于深度学习的图像识别系统，融合本地模型和百度API进行中药材识别。

**核心功能**：
- 图片上传与预处理
- 多模型融合识别
- 识别结果展示与置信度
- 识别历史记录
- 本地模型训练

**相关文件**：
```
apps/image_recognition/
├── models.py           # 数据模型
├── views.py            # 视图函数
├── forms.py            # 表单验证
├── urls.py             # URL路由
├── admin.py            # 后台管理
├── apps.py             # 应用配置
├── models/             # 模型文件目录
│   ├── best_zhongyao.keras           # 训练好的识别模型
│   ├── class_mapping.json            # 类别映射文件
│   ├── best_zhongyao_971.keras       # 旧版模型
│   ├── class_mapping_971.json         # 旧版类别映射
│   ├── medicine_model.pkl            # pickle模型文件
│   └── zhongyao_999/                 # 训练数据集
│       ├── img_0000.jpg
│       ├── img_0001.jpg
│       └── ... (999张训练图片)
├── utils/
│   ├── model_training.py   # 模型训练脚本
│   ├── recognition.py       # 识别核心逻辑
│   └── llm_recognition.py  # 大模型识别辅助
└── templates/image_recognition/
    ├── recognize.html       # 识别上传页面
    └── result.html          # 识别结果页面
```

**数据表**：
- `recognition_record` - 识别记录表
- `medicine_image` - 药材图像库表

**技术实现**：
- 本地模型：TensorFlow/Keras MobileNetV2
- 外部API：百度图像识别API
- 融合策略：本地模型优先，结合百度API结果综合判断

---

### 2.4 销售管理模块（sales）

**功能描述**：提供中药材供应信息、求购信息的发布和管理，以及价格数据查询。

**核心功能**：
- 供应信息发布与管理
- 求购信息发布与管理
- 价格数据展示
- 价格历史记录
- Excel数据导入
- 信息审核功能

**相关文件**：
```
apps/sales/
├── models.py           # 数据模型
├── views.py            # 视图函数
├── forms.py            # 表单验证
├── urls.py             # URL路由
├── admin.py            # 后台管理
├── apps.py             # 应用配置
├── utils/
│   ├── price_crawler.py        # 价格爬虫
│   ├── import_price_data.py    # 价格数据导入
│   └── import_sales_data.py   # 销售数据导入
└── templates/sales/
    ├── index.html              # 销售首页
    ├── supply_list.html        # 供应列表
    ├── supply_detail.html      # 供应详情
    ├── demand_list.html        # 求购列表
    ├── demand_detail.html      # 求购详情
    ├── create_supply.html      # 发布供应
    ├── create_demand.html      # 发布求购
    ├── price_list.html        # 价格列表
    ├── product_list.html     # 商品列表
    ├── product_detail.html   # 商品详情
    ├── cart.html             # 购物车
    └── checkout_success.html # 结账成功
```

**数据表**：
- `supply` - 供应信息表
- `demand` - 求购信息表
- `price_history` - 价格历史表

---

### 2.5 药闻资讯模块（news）

**功能描述**：提供中药材相关新闻和资讯的发布与管理。

**核心功能**：
- 新闻列表展示
- 新闻详情查看
- 新闻分类管理
- 新闻发布与编辑（管理员）

**相关文件**：
```
apps/news/
├── models.py           # 数据模型
├── views.py            # 视图函数
├── urls.py             # URL路由
├── admin.py            # 后台管理
├── apps.py             # 应用配置
└── templates/news/
    ├── news_list.html   # 新闻列表
    └── news_detail.html # 新闻详情
```

**数据表**：
- `news` - 新闻表
- `news_category` - 新闻分类表
- `news_category_rel` - 新闻分类关联表

---

### 2.6 大模型答疑模块（llm_qa）

**功能描述**：基于大模型的智能问答系统，为用户提供中药材相关的专业解答。

**核心功能**：
- 智能问答
- 多轮对话
- 问答历史记录
- GLM-4.7-Flash模型集成

**相关文件**：
```
apps/llm_qa/
├── models.py           # 数据模型
├── views.py            # 视图函数
├── forms.py            # 表单验证
├── urls.py             # URL路由
├── admin.py            # 后台管理
├── apps.py             # 应用配置
├── utils/
│   └── llm_client.py   # 大模型API客户端
└── templates/llm_qa/
    └── ask.html        # 问答页面
```

**数据表**：
- `qa_record` - 问答记录表

---

## 三、系统文件结构

### 3.1 根目录文件

```
zhongyao_system/
├── manage.py                     # Django项目管理入口
├── requirements.txt              # Python依赖清单
├── README.md                     # 项目说明文档
├── .gitignore                    # Git忽略配置
├── db.sqlite3                    # SQLite数据库文件
├── .env                          # 环境变量配置文件
└── sql_scripts/                  # SQL脚本目录
    ├── account.sql              # 用户相关表SQL
    ├── medicine.sql             # 中药材相关表SQL
    ├── sales.sql                # 销售相关表SQL
    ├── news.sql                 # 新闻相关表SQL
    ├── image_recognition.sql    # 图像识别相关表SQL
    ├── llm_qa.sql               # 大模型问答相关表SQL
    ├── full_schema.sql          # 完整SQL架构（长表名）
    └── full_schema_short.sql    # 完整SQL架构（短表名/带注释）
```

### 3.2 核心配置目录

```
zhongyao_system/zhongyao_system/
├── __init__.py
├── settings/                    # 配置目录
│   ├── __init__.py
│   ├── base.py                 # 基础配置
│   ├── dev.py                  # 开发环境配置
│   └── prod.py                 # 生产环境配置
├── urls.py                     # 主URL配置
├── asgi.py                     # ASGI配置
└── wsgi.py                     # WSGI配置
```

### 3.3 静态文件目录

```
zhongyao_system/static/
├── css/
│   └── style.css              # 自定义样式
├── js/
│   └── main.js                # 主要JavaScript
├── plugins/                   # 插件目录
│   └── js/
│       └── main.js           # 插件JavaScript
└── data/                      # 数据文件
    ├── 中药材.csv             # 中药材数据
    ├── 中药材供应信息.xlsx     # 供应信息
    ├── 中药材求购信息.xlsx     # 求购信息
    ├── 中药材图片.csv         # 药材图片数据
    ├── 方剂.csv               # 方剂数据
    ├── 方剂图片.csv           # 方剂图片数据
    ├── 药膳食疗.csv           # 药膳数据
    ├── 药膳食疗图片.csv       # 药膳图片数据
    ├── 针灸穴位.csv           # 穴位数据
    └── 针灸穴位图片_new.csv   # 穴位图片数据
```

### 3.4 模板文件目录

```
zhongyao_system/templates/
├── base.html                   # 基础模板
├── 404.html                    # 404错误页面
└── 500.html                    # 500错误页面
```

---

## 四、技术架构

### 4.1 技术栈

**后端技术**：
- Python 3.12+
- Django 4.2+
- Django ORM
- SQLite/MySQL

**前端技术**：
- HTML5
- CSS3
- JavaScript (ES6+)
- Bootstrap 5
- Font Awesome 6

**人工智能**：
- TensorFlow/Keras
- 百度图像识别API
- 智谱GLM-4.7-Flash大模型

**数据处理**：
- Pandas
- NumPy
- Pillow

### 4.2 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                        用户界面层                            │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐   │
│  │  首页    │ 中药材   │ 图像识别 │ 药闻资讯 │ 大模型答疑 │   │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘   │
├─────────────────────────────────────────────────────────────┤
│                        业务逻辑层                            │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐   │
│  │ 用户管理 │ 药材管理 │ 图像识别 │ 销售管理 │ 智能问答 │   │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘   │
├─────────────────────────────────────────────────────────────┤
│                        数据访问层                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                    Django ORM                          │  │
│  └──────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│                        数据存储层                            │
│  ┌────────────┬────────────┬────────────┬────────────┐      │
│  │  SQLite   │   文件存储  │  模型文件   │  API服务   │      │
│  └────────────┴────────────┴────────────┴────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 数据库设计

系统采用关系型数据库设计，包含以下主要表关系：

```
auth_user (用户表)
    │
    ├── account_profile (用户资料)
    ├── supply (供应信息) ─── medicine (中药材)
    ├── demand (求购信息)
    ├── recognition_record (识别记录)
    ├── qa_record (问答记录)
    └── news (新闻) ─── news_category (分类)

price_history (价格历史) ─── supply (供应信息)
```

---

## 五、部署说明

### 5.1 环境要求

- Python 3.12 或更高版本
- pip 包管理工具
- Git 版本控制
- 内存：推荐 4GB+
- 磁盘：推荐 10GB+

### 5.2 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd zhongyao_system
```

2. **创建虚拟环境**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置环境变量**
```bash
# 创建 .env 文件
touch .env

# 编辑 .env 内容
DATABASE_URL=sqlite:///db.sqlite3
BAIDU_API_KEY=your_baidu_api_key
BAIDU_SECRET_KEY=your_baidu_secret_key
GLM_API_KEY=your_glm_api_key
SECRET_KEY=your_django_secret_key
DEBUG=True
```

5. **数据库迁移**
```bash
python manage.py migrate
```

6. **创建管理员**
```bash
python manage.py createsuperuser
```

7. **运行服务器**
```bash
python manage.py runserver
```

### 5.3 生产环境部署

对于生产环境，建议使用：
- Gunicorn + Nginx
- MySQL/PostgreSQL 替代 SQLite
- 配置 HTTPS
- 设置防火墙规则

---

## 六、API接口说明

### 6.1 图像识别接口

**请求方式**：POST
**URL**：`/image_recognition/recognize/`
**参数**：
- image: 图片文件

**响应示例**：
```json
{
    "success": true,
    "result": {
        "name": "人参",
        "confidence": 0.95,
        "alternatives": [
            {"name": "党参", "confidence": 0.72},
            {"name": "西洋参", "confidence": 0.65}
        ]
    }
}
```

### 6.2 大模型问答接口

**请求方式**：POST
**URL**：`/llm_qa/ask/`
**参数**：
- question: 问题内容

**响应示例**：
```json
{
    "success": true,
    "answer": "人参具有大补元气、补脾益肺、生津止渴、安神益智的功效...",
    "model_used": "GLM-4.7-Flash"
}
```

---

## 七、数据库表结构

### 7.1 用户相关表

| 表名 | 说明 | 主要字段 |
|------|------|----------|
| auth_user | 用户表 | id, username, password, email, is_staff, is_active |
| account_profile | 用户资料表 | id, user_id, avatar, bio, phone |

### 7.2 中药材相关表

| 表名 | 说明 | 主要字段 |
|------|------|----------|
| medicine | 中药材表 | id, name, latin_name, category, origin, properties, functions |
| prescription | 方剂表 | id, name, ingredients, dosage, preparation, functions |
| dietary | 药膳食疗表 | id, name, ingredients, preparation, functions |
| acupuncture | 针灸穴位表 | id, name, location, functions, indications, method |

### 7.3 销售相关表

| 表名 | 说明 | 主要字段 |
|------|------|----------|
| supply | 供应信息表 | id, medicine_name, specification, quantity, price, location |
| demand | 求购信息表 | id, medicine_name, specification, quantity, price |
| price_history | 价格历史表 | id, medicine_name, specification, date, price |

### 7.4 其他表

| 表名 | 说明 | 主要字段 |
|------|------|----------|
| news | 新闻表 | id, title, content, author, publish_date, is_published |
| recognition_record | 识别记录表 | id, user_id, image, result, confidence |
| qa_record | 问答记录表 | id, user_id, question, answer, model_used |

---

## 八、系统亮点

1. **多模型融合识别**
   - 结合本地TensorFlow模型和百度API
   - 提高中药材识别准确率

2. **大模型智能问答**
   - 基于GLM-4.7-Flash模型
   - 支持多轮对话上下文理解

3. **全中文界面**
   - 包括管理后台在内的全中文界面
   - 提升用户体验

4. **响应式设计**
   - 支持桌面端、平板端、移动端
   - Bootstrap 5响应式布局

5. **模块化架构**
   - 清晰的Django应用分离
   - 便于维护和扩展

6. **完善的后台管理**
   - Django Admin全中文后台
   - 统一管理所有数据

---

## 九、注意事项

### 9.1 开发注意

- 修改模型后需执行 `python manage.py makemigrations` 和 `python manage.py migrate`
- 上传文件需配置好 MEDIA_ROOT 和 MEDIA_URL
- 生产环境请修改 SECRET_KEY 和 DEBUG 设置

### 9.2 安全建议

- 生产环境务必使用 HTTPS
- 定期备份数据库
- 保护好 API 密钥
- 及时更新依赖包版本

### 9.3 性能优化

- 大文件上传建议限制大小
- 图片识别建议限制并发
- 数据库查询注意索引
- 静态文件建议使用 CDN

---

## 十、联系方式

- 邮箱：contact@zhongyao.com
- 电话：400-123-4567
- 地址：北京市朝阳区

---

**文档版本**：V1.0
**最后更新**：2026年4月
**编写目的**：为开发者提供完整的系统说明和开发指南