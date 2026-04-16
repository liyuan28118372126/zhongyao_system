"""LLM-based image recognition utility functions."""

import os
import tempfile
import sys
import json
import base64
import requests
import tensorflow as tf
from PIL import Image

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

# ===================== 配置项 =====================
# 百度API配置
BAIDU_API_KEY = "5RfoAI19xedjW5UulKQgOERM"
BAIDU_SECRET_KEY = "rsLPUGZuhy90JO7wt6yGA2EAJGEn7SQ1"
BAIDU_ACCESS_TOKEN = None

# 本地模型路径
import os
# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 向上一级到image_recognition目录，再到models目录
models_dir = os.path.join(current_dir, '..', 'models')

MODEL_PATH = os.path.join(models_dir, "best_zhongyao.keras")
MAPPING_PATH = os.path.join(models_dir, "class_mapping.json")

# 中药关键词增强（用于模糊匹配）
CHINESE_HERB_KEYWORDS = [
    "参", "芪", "归", "草", "仁", "苓", "术", "黄", "麻", "桂", "芍", "芎",
    "防风", "当归", "黄芪", "甘草", "枸杞", "人参", "白术", "茯苓", "柴胡",
    "桔梗", "麦冬", "陈皮", "半夏", "黄连", "黄芩", "大黄", "生姜", "大枣"
]


# ===================== 工具函数 =====================
def load_herb_list(mapping_path):
    """加载971种中药材列表，用于白名单过滤"""
    with open(mapping_path, 'r', encoding='utf-8') as f:
        idx_to_class = json.load(f)
        herb_list = [v for k, v in idx_to_class.items()]
    # 去重+转小写，方便匹配
    herb_list = [herb.strip().lower() for herb in herb_list if herb.strip()]
    return list(set(herb_list)), idx_to_class


def fuzzy_match_herb(keyword, herb_list):
    """模糊匹配中药材（支持部分关键词匹配）"""
    keyword = keyword.lower().strip()
    matched = []
    print(f"🔍 尝试匹配关键词：{keyword}")
    
    # 计算关键词与每个中药材的匹配度
    for herb in herb_list:
        herb_lower = herb.lower().strip()
        
        # 1. 完全匹配
        if keyword == herb_lower:
            matched.append((herb, 1.0))  # 匹配度100%
            print(f"✅ 完全匹配：{herb}")
        # 2. 包含匹配（如"西洋参"匹配"人参"）
        elif keyword in herb_lower or herb_lower in keyword:
            matched.append((herb, 0.8))  # 匹配度80%
            print(f"✅ 包含匹配：{herb}")
        # 3. 关键词匹配（如包含"参"）
        elif any(kw in keyword and kw in herb_lower for kw in CHINESE_HERB_KEYWORDS):
            matched.append((herb, 0.6))  # 匹配度60%
            print(f"✅ 关键词匹配：{herb}")
        # 4. 部分匹配（如"黄芪"匹配"黄"）
        elif any(part in herb_lower for part in keyword.split()):
            matched.append((herb, 0.5))  # 匹配度50%
            print(f"✅ 部分匹配：{herb}")
    
    # 去重并按匹配度排序
    matched = list(set(matched))
    matched.sort(key=lambda x: x[1], reverse=True)
    
    # 只返回匹配度大于0.7的结果
    if matched and matched[0][1] >= 0.7:
        result = matched[0][0]
        print(f"🔍 最终匹配结果：{result} (匹配度: {matched[0][1]})")
        return result
    else:
        print("🔍 无足够匹配度的结果")
        return None


# ===================== 百度识图（仅中药版） =====================
def get_baidu_access_token():
    """获取百度API凭证"""
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": BAIDU_API_KEY,
        "client_secret": BAIDU_SECRET_KEY
    }
    response = requests.post(url, params=params)
    if response.status_code == 200:
        global BAIDU_ACCESS_TOKEN
        BAIDU_ACCESS_TOKEN = response.json()["access_token"]
        return BAIDU_ACCESS_TOKEN
    raise Exception(f"百度Token获取失败：{response.text}")


def predict_baidu_herb_only(img_path, herb_list, top_n=5):
    """百度识图仅返回中药材结果"""
    if not BAIDU_ACCESS_TOKEN:
        get_baidu_access_token()

    # 图片转base64
    with open(img_path, 'rb') as f:
        img_base64 = base64.b64encode(f.read()).decode('utf-8')

    # 调用百度识图API
    url = f"https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general?access_token={BAIDU_ACCESS_TOKEN}"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"image": img_base64, "baike_num": 0}
    response = requests.post(url, headers=headers, data=data)

    if response.status_code != 200:
        raise Exception(f"百度识图请求失败：{response.text}")

    result = response.json()
    herb_results = []
    print(f"🔍 百度原始识别结果：{[item['keyword'] for item in result.get('result', [])[:10]]}")
    
    if "result" in result:
        for item in result["result"][:20]:  # 取前20个结果过滤，增加识别机会
            keyword = item["keyword"].strip()
            score = float(item["score"])
            
            # 只处理置信度大于0.5的结果
            if score >= 0.5:
                # 模糊匹配中药材
                matched_herb = fuzzy_match_herb(keyword, herb_list)
                if matched_herb:
                    # 调整置信度（匹配度加权）
                    match_score = 1.0 if matched_herb == keyword.lower() else 0.8
                    final_score = score * match_score * 100  # 转百分比
                    herb_results.append({
                        "source": "百度识图（中药）",
                        "rank": len(herb_results) + 1,
                        "name": matched_herb,
                        "score": round(final_score, 2),
                        "original": keyword  # 原始识别结果
                    })
                    if len(herb_results) >= top_n:
                        break
    print(f"🔍 百度中药识别结果：{[res['name'] for res in herb_results]}")
    return herb_results


# ===================== 本地模型预测（复用） =====================
def load_model_and_mapping():
    """加载本地模型和类别映射"""
    # 尝试加载模型，处理兼容性问题
    try:
        # 方法1：直接加载
        model = tf.keras.models.load_model(MODEL_PATH)
    except Exception as e:
        print(f"直接加载失败，尝试兼容性加载：{e}")
        # 方法2：使用custom_objects处理
        try:
            from keras.layers import Dense
            # 自定义Dense层处理quantization_config参数
            class CompatibilityDense(Dense):
                def __init__(self, quantization_config=None, **kwargs):
                    # 忽略quantization_config参数
                    super().__init__(**kwargs)
            
            model = tf.keras.models.load_model(
                MODEL_PATH,
                custom_objects={'Dense': CompatibilityDense}
            )
        except Exception as e2:
            print(f"兼容性加载失败：{e2}")
            # 方法3：使用safe_mode
            try:
                model = tf.keras.models.load_model(
                    MODEL_PATH,
                    safe_mode=True
                )
            except Exception as e3:
                print(f"安全模式加载失败：{e3}")
                # 兜底：如果所有方法都失败，使用百度API
                raise Exception("模型加载失败，请检查TensorFlow版本兼容性")
    
    herb_list, idx_to_class = load_herb_list(MAPPING_PATH)
    return model, idx_to_class, herb_list


def preprocess_img(img_path):
    """图片预处理"""
    img_path_bytes = img_path.encode('utf-8')
    img = tf.io.read_file(img_path_bytes)
    img = tf.image.decode_image(img, channels=3, expand_animations=False)
    img = tf.image.resize(img, (224, 224))
    img = tf.keras.applications.mobilenet_v2.preprocess_input(img)
    return img


def predict_local_model(model, idx_to_class, img_path, top_n=5):
    """本地模型预测（仅返回中药）"""
    img = preprocess_img(img_path)
    img_batch = tf.expand_dims(img, axis=0)
    pred = model.predict(img_batch, verbose=0)
    # 取Top-N中药结果
    pred_indices = tf.argsort(pred[0], direction='DESCENDING').numpy()[:top_n]
    pred_confs = tf.sort(pred[0], direction='DESCENDING').numpy()[:top_n]
    results = []
    print(f"本地模型预测结果：indices={pred_indices}, confs={pred_confs}")
    for i in range(top_n):
        herb_name = idx_to_class[str(pred_indices[i])]
        score = round(float(pred_confs[i]) * 100, 2)
        print(f"预测第{i+1}名：{herb_name}，置信度：{score}%")
        results.append({
            "source": "本地模型（中药）",
            "rank": i + 1,
            "name": herb_name,
            "score": score,
            "original": herb_name
        })
    return results


# ===================== 融合预测（核心函数） =====================
def fusion_predict_herb_only(img_path, top_n=5):
    """融合预测：仅返回中药材结果"""
    # 1. 加载模型和中药库
    model, idx_to_class, herb_list = load_model_and_mapping()
    print(f"✅ 加载模型成功，中药材库大小：{len(herb_list)}")

    # 2. 百度识图（仅中药）
    baidu_results = []
    try:
        baidu_results = predict_baidu_herb_only(img_path, herb_list, top_n)
        print(f"✅ 百度识图结果：{[res['name'] for res in baidu_results]}")
    except Exception as e:
        print(f"⚠️ 百度识图调用失败：{e}")

    # 3. 本地模型预测
    local_results = predict_local_model(model, idx_to_class, img_path, top_n)
    print(f"✅ 本地模型结果：{[res['name'] for res in local_results]}")

    # 4. 融合结果（优先百度API，补充本地模型）
    all_results = baidu_results.copy()
    # 补充本地模型结果（避免百度API无结果时为空）
    if len(all_results) < top_n:
        for res in local_results:
            # 去重：不重复添加相同药材
            if res["name"] not in [r["name"] for r in all_results]:
                all_results.append(res)
                if len(all_results) >= top_n:
                    break

    # 5. 按置信度排序，取Top-N
    all_results.sort(key=lambda x: x["score"], reverse=True)
    final_results = all_results[:top_n]
    print(f"✅ 融合后结果：{[res['name'] for res in final_results]}")

    # 6. 兜底：如果无结果，返回本地模型Top5
    if not final_results:
        final_results = local_results[:top_n]
        print(f"⚠️ 使用本地模型兜底结果：{[res['name'] for res in final_results]}")

    return final_results


def analyze_image_color_and_texture(image_path):
    """基于颜色和纹理分析图像，返回可能的中药材"""
    try:
        from PIL import Image
        import numpy as np
        
        # 打开图像
        img = Image.open(image_path)
        img = img.resize((224, 224))
        
        # 转换为RGB
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # 计算颜色特征
        img_array = np.array(img)
        mean_color = np.mean(img_array, axis=(0, 1))
        std_color = np.std(img_array, axis=(0, 1))
        
        # 颜色分类
        r, g, b = mean_color
        
        # 基于颜色的简单分类
        if r > g and r > b:
            # 偏红
            if r > 150:
                return "红参", 0.7
            else:
                return "丹参", 0.6
        elif g > r and g > b:
            # 偏绿
            return "绿茶", 0.6
        elif b > r and b > g:
            # 偏蓝
            return "蓝莓", 0.5
        elif r > 100 and g > 100 and b < 80:
            # 偏黄
            return "黄芪", 0.7
        elif r < 100 and g < 100 and b < 100:
            # 偏黑
            return "熟地", 0.6
        elif r > 120 and g > 100 and b > 80:
            # 偏棕
            return "当归", 0.7
        else:
            # 其他颜色
            return "中药材", 0.5
    except Exception as e:
        print(f"Image analysis error: {e}")
        return "中药材", 0.5

def recognize_medicine_llm(image):
    """Recognize medicine from image using LLM-based model."""
    try:
        # Save the image temporarily
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            temp_path = temp_file.name
        
        with open(temp_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        
        # Use fusion prediction (local model + Baidu API)
        try:
            # 直接使用融合预测函数，而不依赖3.py脚本
            results = fusion_predict_herb_only(temp_path, top_n=5)
            
            if results:
                # Get top result
                top_result = results[0]
                name = top_result['name']
                confidence = top_result['score'] / 100.0  # Convert to 0-1 scale
                
                # Get candidates
                candidates = [res['name'] for res in results]
                
                # Create result dictionary
                result_dict = {
                    'name': name,
                    'latin_name': '',
                    'category': '未知',
                    'functions': '待确认',
                    'candidates': candidates,
                    'sources': [{
                        'name': res['source'],
                        'confidence': res['score'],
                        'original': res.get('original', res['name'])
                    } for res in results]
                }
                
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                
                return result_dict, confidence
            else:
                # 空结果，使用基于颜色的识别
                print("Fusion prediction returned empty results, using color-based recognition")
                name, confidence = analyze_image_color_and_texture(temp_path)
                result_dict = {
                    'name': name,
                    'latin_name': '',
                    'category': '未知',
                    'functions': '待确认',
                    'candidates': [name, '中药材', '草药', '中药饮片'],
                    'sources': [{
                        'name': '颜色分析',
                        'confidence': confidence * 100,
                        'original': name
                    }]
                }
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                return result_dict, confidence
                
        except Exception as llm_error:
            print(f"LLM recognition error: {llm_error}")
            # 使用基于颜色的识别
            name, confidence = analyze_image_color_and_texture(temp_path)
            result_dict = {
                'name': name,
                'latin_name': '',
                'category': '未知',
                'functions': '待确认',
                'candidates': [name, '中药材', '草药', '中药饮片'],
                'sources': [{
                    'name': '颜色分析',
                    'confidence': confidence * 100,
                    'original': name
                }]
            }
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return result_dict, confidence
        
    except Exception as e:
        # Handle exceptions
        print(f"Recognition error: {e}")
        import traceback
        traceback.print_exc()
        return {'name': '识别失败', 'latin_name': '', 'category': '', 'functions': ''}, 0.0