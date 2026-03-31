import os
import zipfile
import json
import math
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.preprocessing.image import random_rotation
import matplotlib.pyplot as plt

# ===================== 【本地路径】你刚刚生成的文件 =====================
ZIP_FILE_NAME = r"训练包种中药材.zip"
LABEL_FILE_NAME = r"训练标注中药材.csv"

# 本地解压目录
UNZIP_DIR = r"D:\Python\pycharm\pythonProject1\llm\zhongyao_999"
OUTPUT_MODEL = r"D:\Python\pycharm\pythonProject1\llm\best_zhongyao.keras"
OUTPUT_CLASS = r"D:\Python\pycharm\pythonProject1\llm\class_mapping.json"

# ===================== 1. 检查文件 =====================
print("=== 第一步：检查文件 ===")

if not os.path.exists(ZIP_FILE_NAME):
    raise Exception(f"找不到压缩包：{ZIP_FILE_NAME}")
if not os.path.exists(LABEL_FILE_NAME):
    raise Exception(f"找不到标注文件：{LABEL_FILE_NAME}")

print("✅ 文件检查完成！")

# ===================== 2. 解压 =====================
print("\n=== 第二步：解压数据 ===")
os.makedirs(UNZIP_DIR, exist_ok=True)

with zipfile.ZipFile(ZIP_FILE_NAME, 'r') as zipf:
    zipf.extractall(UNZIP_DIR)

img_count = len([f for f in os.listdir(UNZIP_DIR) if f.endswith(('.jpg', '.png'))])
print(f"✅ 解压完成！共 {img_count} 张图片")

# ===================== 3. 构建数据集 =====================
print("\n=== 第三步：构建数据集 ===")
df = pd.read_csv(LABEL_FILE_NAME, encoding='utf-8')

classes = df["label"].unique().tolist()
num_classes = len(classes)
class_to_idx = {cls: idx for idx, cls in enumerate(classes)}
idx_to_class = {v: k for k, v in class_to_idx.items()}

with open(OUTPUT_CLASS, 'w', encoding='utf-8') as f:
    json.dump(idx_to_class, f, ensure_ascii=False)

print(f"✅ 类别数：{num_classes}")

image_paths = []
labels = []
for _, row in df.iterrows():
    img_path = os.path.join(UNZIP_DIR, row["image"])
    if os.path.exists(img_path):
        image_paths.append(img_path)
        labels.append(class_to_idx[row["label"]])

print(f"✅ 有效数据：{len(image_paths)} 条")

# 划分
train_ratio = 0.8
train_size = int(len(image_paths) * train_ratio)

train_paths = image_paths[:train_size]
train_labels = labels[:train_size]
val_paths = image_paths[train_size:]
val_labels = labels[train_size:]

print(f"训练集：{len(train_paths)}")
print(f"验证集：{len(val_paths)}")


# ===================== 数据增强 =====================
def augment_img(img):
    img = tf.image.random_flip_left_right(img)
    img = tf.image.random_flip_up_down(img)
    img = tf.image.random_brightness(img, max_delta=0.2)
    img = tf.image.random_contrast(img, 0.8, 1.2)

    img_np = img.numpy()
    img_np = random_rotation(img_np, rg=10, row_axis=0, col_axis=1, channel_axis=2)
    return tf.convert_to_tensor(img_np, dtype=tf.float32)


def load_train_img(path, label):
    img = tf.io.read_file(path)
    img = tf.image.decode_image(img, channels=3, expand_animations=False)
    img = tf.image.resize(img, (224, 224))
    img = tf.py_function(augment_img, [img], tf.float32)
    img.set_shape((224, 224, 3))
    img = tf.keras.applications.mobilenet_v2.preprocess_input(img)
    return img, label


def load_val_img(path, label):
    img = tf.io.read_file(path)
    img = tf.image.decode_image(img, channels=3, expand_animations=False)
    img = tf.image.resize(img, (224, 224))
    img = tf.keras.applications.mobilenet_v2.preprocess_input(img)
    return img, label


# 数据集
batch_size = 8
train_ds = tf.data.Dataset.from_tensor_slices((train_paths, train_labels))
train_ds = train_ds.map(load_train_img, num_parallel_calls=tf.data.AUTOTUNE)
train_ds = train_ds.shuffle(100).batch(batch_size).repeat().prefetch(tf.data.AUTOTUNE)

val_ds = tf.data.Dataset.from_tensor_slices((val_paths, val_labels))
val_ds = val_ds.map(load_val_img).batch(batch_size).prefetch(tf.data.AUTOTUNE)

steps_per_epoch = math.ceil(len(train_paths) / batch_size)
validation_steps = math.ceil(len(val_paths) / batch_size)

# ===================== 训练模型 =====================
print("\n=== 第四步：开始训练 ===")

base_model = tf.keras.applications.MobileNetV2(
    input_shape=(224, 224, 3), weights="imagenet", include_top=False
)

base_model.trainable = True
for layer in base_model.layers[:-10]:
    layer.trainable = False

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.BatchNormalization(),
    layers.Dense(1024, activation='relu'),
    layers.Dropout(0.5),
    layers.BatchNormalization(),
    layers.Dense(512, activation='relu'),
    layers.Dropout(0.4),
    layers.Dense(num_classes, activation='softmax')
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-4),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

callbacks = [
    ModelCheckpoint(OUTPUT_MODEL, monitor='val_loss', save_best_only=True),
    ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=4),
    EarlyStopping(monitor='val_loss', patience=8, restore_best_weights=True)
]

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=30,
    steps_per_epoch=steps_per_epoch,
    validation_steps=validation_steps,
    callbacks=callbacks
)

# ===================== 训练完成 =====================
print("\n🏁 训练完成！")
print(f"模型已保存：{OUTPUT_MODEL}")
print(f"类别映射：{OUTPUT_CLASS}")

# 绘图
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='训练准确率')
plt.plot(history.history['val_accuracy'], label='验证准确率')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='训练损失')
plt.plot(history.history['val_loss'], label='验证损失')
plt.legend()
plt.show()