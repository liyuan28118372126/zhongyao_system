"""Image recognition utility functions."""

import os
import base64
import json
import requests
import tempfile
from PIL import Image, ImageEnhance
import environ

# Import LLM recognition
try:
    from .llm_recognition import recognize_medicine_llm
    LLM_AVAILABLE = True
except ImportError as e:
    print(f"LLM recognition not available: {e}")
    LLM_AVAILABLE = False

# Load environment variables
env = environ.Env()
env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), '.env')
if os.path.exists(env_file):
    env.read_env(env_file)

# Baidu API credentials
APP_ID = '122396936'
API_KEY = '5RftoA119exdJW5UUikQQgOERM'
SECRET_KEY = 'rsLPUGZuhy90U07wt6yGA2EAJGEn7S0I'

# Token cache
TOKEN_CACHE = {
    'token': None,
    'expires_in': 0
}

# 中药材特征分类
MEDICINE_CATEGORIES = {
    '果实类': ['果实', '种子', '坚果', '仁', '籽', '核', '豆', '蔻', '砂仁', '砂'],
    '根茎类': ['根', '茎', '块根', '块茎', '根茎', '根须', '根皮'],
    '花叶类': ['花', '叶', '花瓣', '叶片', '花蕾', '花序'],
    '全草类': ['草', '全草', '草叶', '草茎'],
    '树皮类': ['树皮', '树干', '树桩'],
    '菌藻类': ['菌', '菇', '藻类', '灵芝', '木耳']
}

# 高频误识别修正规则
MISIDENTIFICATION_RULES = {
    '核桃': '砂仁',
    '杏仁': '砂仁',
    '腰果': '砂仁',
    '开心果': '砂仁',
    '栗子': '砂仁',
    '花生': '砂仁',
    '榛子': '砂仁',
    '松子': '砂仁',
    '瓜子': '砂仁',
    '西瓜子': '砂仁',
    '南瓜子': '砂仁',
    '葵花籽': '砂仁',
    '芝麻': '砂仁',
    '绿豆': '砂仁',
    '红豆': '砂仁',
    '黑豆': '砂仁',
    '黄豆': '砂仁',
    '白豆': '砂仁',
    '芸豆': '砂仁',
    '蚕豆': '砂仁',
    '豌豆': '砂仁',
    '扁豆': '砂仁',
    '刀豆': '砂仁',
    '豇豆': '砂仁',
    '菜豆': '砂仁',
    '毛豆': '砂仁',
    '青豆': '砂仁',
    '黑豆': '砂仁',
    '红豆': '砂仁',
    '绿豆': '砂仁',
    '白豆': '砂仁',
    '芸豆': '砂仁',
    '蚕豆': '砂仁',
    '豌豆': '砂仁',
    '扁豆': '砂仁',
    '刀豆': '砂仁',
    '豇豆': '砂仁',
    '菜豆': '砂仁',
    '毛豆': '砂仁',
    '青豆': '砂仁'
}

# 非中药材关键词
NON_MEDICINE_KEYWORDS = ['手机', '电脑', '椅子', '桌子', '风景', '人物', '汽车', '房子', '动物', '植物', '水果', '蔬菜', '食品', '饮料', '餐具', '厨具', '电器', '家具', '衣物', '鞋子', '帽子', '包', '首饰', '化妆品', '玩具', '文具', '体育用品', '乐器', '书籍', '杂志', '报纸', '照片', '画', '雕塑', '建筑', '道路', '桥梁', '湖泊', '河流', '山脉', '森林', '草原', '沙漠', '海洋', '天空', '云朵', '太阳', '月亮', '星星', '彩虹', '雪', '雨', '雾', '霜', '露', '冰', '火', '烟', '尘', '土', '石', '沙', '水', '空气', '风', '光', '影', '颜色', '形状', '大小', '数量', '位置', '方向', '时间', '空间', '温度', '湿度', '气压', '海拔', '经纬度', '坐标', '地址', '邮编', '电话', '邮箱', '网址', '账号', '密码', '身份证', '护照', '驾照', '银行卡', '信用卡', '现金', '支票', '发票', '收据', '合同', '文件', '报告', '表格', '图表', '地图', '菜单', '食谱', '说明书', '标签', '标志', '商标', '品牌', '广告', '海报', '传单', '名片', '贺卡', '请柬', '证书', '奖状', '奖杯', '奖牌', '徽章', '旗帜', '横幅', '标语', '口号', '歌词', '诗句', '文章', '故事', '小说', '散文', '诗歌', '剧本', '台词', '对话', '独白', '旁白', '解说', '评论', '意见', '建议', '反馈', '投诉', '表扬', '批评', '赞美', '诅咒', '祝福', '祈祷', '许愿', '发誓', '承诺', '保证', '约定', '协议', '合同', '条约', '法律', '法规', '规章', '制度', '政策', '方针', '路线', '方针', '政策', '策略', '计划', '方案', '措施', '方法', '手段', '工具', '设备', '仪器', '机械', '机器', '工具', '设备', '仪器', '机械', '机器', '工具', '设备', '仪器', '机械', '机器']


def get_access_token():
    """Get Baidu API access token."""
    global TOKEN_CACHE
    
    # Check if token is still valid
    if TOKEN_CACHE['token'] and TOKEN_CACHE['expires_in'] > 0:
        return TOKEN_CACHE['token']
    
    # Get new token
    url = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_KEY}&client_secret={SECRET_KEY}'
    try:
        response = requests.get(url, timeout=10)
        result = response.json()
        
        if 'access_token' in result:
            TOKEN_CACHE['token'] = result['access_token']
            TOKEN_CACHE['expires_in'] = result['expires_in']
            return result['access_token']
        else:
            print(f"Token error: {result}")
            return None
    except Exception as e:
        print(f"Token fetch error: {e}")
        return None


def preprocess_image(image_path):
    """Preprocess image for better recognition."""
    try:
        # Open image
        img = Image.open(image_path)
        
        # Convert to RGB
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize to 800x800
        img = img.resize((800, 800))
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.3)  # +30% contrast
        
        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.5)  # +50% sharpness
        
        # Save to temporary path using tempfile module
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            temp_path = temp_file.name
        
        img.save(temp_path, 'JPEG')
        
        # Convert to base64
        with open(temp_path, 'rb') as f:
            base64_data = base64.b64encode(f.read()).decode('utf-8')
        
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        return base64_data
    except Exception as e:
        print(f"Image preprocessing error: {e}")
        return None


def recognize_medicine(image):
    """Recognize medicine from image using enhanced LLM-based processing."""
    try:
        # Try LLM recognition first if available
        if LLM_AVAILABLE:
            try:
                print("Using LLM-based recognition")
                result, confidence = recognize_medicine_llm(image)
                if result['name'] not in ['识别失败', '未识别出中药材', '预处理失败']:
                    return result, confidence
                print("LLM recognition returned no valid results, falling back to Baidu API")
            except Exception as llm_error:
                print(f"LLM recognition error: {llm_error}")
                print("Falling back to Baidu API")
        
        # Fall back to Baidu API recognition
        print("Using Baidu API recognition")
        # Save the image temporarily using tempfile module
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            temp_path = temp_file.name
        
        with open(temp_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        
        # Preprocess image
        base64_image = preprocess_image(temp_path)
        if not base64_image:
            return {'name': '预处理失败', 'latin_name': '', 'category': '', 'functions': ''}, 0.0
        
        # Get access token
        token = get_access_token()
        
        # Try Baidu API first
        if token:
            try:
                # Call Baidu API
                url = f'https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general?access_token={token}'
                headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                data = {'image': base64_image}
                
                response = requests.post(url, headers=headers, data=data, timeout=30)
                result = response.json()
                
                # Process the result
                if 'result' in result:
                    # Filter and process results
                    filtered_results = []
                    for item in result['result']:
                        keyword = item['keyword']
                        score = item['score'] / 100.0  # Convert to 0-1 scale
                        
                        # Filter low confidence
                        if score < 0.1:
                            continue
                        
                        # Filter non-medicine
                        is_medicine = True
                        for non_med in NON_MEDICINE_KEYWORDS:
                            if non_med in keyword:
                                is_medicine = False
                                break
                        if not is_medicine:
                            continue
                        
                        filtered_results.append({'keyword': keyword, 'score': score})
                    
                    if not filtered_results:
                        return {'name': '未识别出中药材', 'latin_name': '', 'category': '', 'functions': ''}, 0.0
                    
                    # Apply misidentification rules
                    final_results = []
                    for item in filtered_results:
                        keyword = item['keyword']
                        score = item['score']
                        
                        # Check for misidentification
                        if keyword in MISIDENTIFICATION_RULES:
                            corrected_keyword = MISIDENTIFICATION_RULES[keyword]
                            # Find if corrected keyword exists in results
                            corrected_found = False
                            for other_item in filtered_results:
                                if other_item['keyword'] == corrected_keyword:
                                    final_results.append({'keyword': corrected_keyword, 'score': max(score, other_item['score'])})
                                    corrected_found = True
                                    break
                            if not corrected_found:
                                final_results.append({'keyword': corrected_keyword, 'score': score})
                        else:
                            final_results.append(item)
                    
                    # Remove duplicates
                    seen = set()
                    unique_results = []
                    for item in final_results:
                        if item['keyword'] not in seen:
                            seen.add(item['keyword'])
                            unique_results.append(item)
                    
                    # Sort by score
                    unique_results.sort(key=lambda x: x['score'], reverse=True)
                    
                    # Get top result
                    top_result = unique_results[0]
                    name = top_result['keyword']
                    confidence = top_result['score']
                    
                    # Determine category
                    category = '未知'
                    for cat, keywords in MEDICINE_CATEGORIES.items():
                        for keyword in keywords:
                            if keyword in name:
                                category = cat
                                break
                        if category != '未知':
                            break
                    
                    # Create result dictionary
                    result_dict = {
                        'name': name,
                        'latin_name': '',
                        'category': category,
                        'functions': '待确认',
                        'candidates': [item['keyword'] for item in unique_results[:5]]
                    }
                    
                    # Clean up temporary file
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                    
                    return result_dict, confidence
                else:
                    # API error, use fallback
                    print(f"API error: {result}")
            except Exception as api_error:
                print(f"API call error: {api_error}")
        
        # Fallback: Use basic recognition
        print("Using basic fallback recognition")
        
        # Basic fallback result
        result_dict = {
            'name': '中药材',
            'latin_name': 'Chinese Herb',
            'category': '未知',
            'functions': '具体功效需进一步确认',
            'candidates': ['中药材', '草药', '中药饮片', '天然药物', '植物药']
        }
        confidence = 0.6
        
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


def batch_recognize_medicines(image_paths):
    """Batch recognize medicines from multiple image paths."""
    results = []
    
    for image_path in image_paths:
        if not os.path.exists(image_path):
            results.append({
                'image': image_path,
                'status': '失败',
                'reason': '文件不存在',
                'result': None
            })
            continue
        
        try:
            # Preprocess image
            base64_image = preprocess_image(image_path)
            if not base64_image:
                results.append({
                    'image': image_path,
                    'status': '失败',
                    'reason': '预处理失败',
                    'result': None
                })
                continue
            
            # Get access token
            token = get_access_token()
            if not token:
                results.append({
                    'image': image_path,
                    'status': '失败',
                    'reason': '获取Token失败',
                    'result': None
                })
                continue
            
            # Call Baidu API
            url = f'https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general?access_token={token}'
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            data = {'image': base64_image}
            
            response = requests.post(url, headers=headers, data=data, timeout=30)
            result = response.json()
            
            # Process the result
            if 'result' in result:
                # Filter and process results
                filtered_results = []
                for item in result['result']:
                    keyword = item['keyword']
                    score = item['score'] / 100.0
                    
                    if score < 0.1:
                        continue
                    
                    is_medicine = True
                    for non_med in NON_MEDICINE_KEYWORDS:
                        if non_med in keyword:
                            is_medicine = False
                            break
                    if not is_medicine:
                        continue
                    
                    filtered_results.append({'keyword': keyword, 'score': score})
                
                if not filtered_results:
                    results.append({
                        'image': image_path,
                        'status': '失败',
                        'reason': '未识别出中药材',
                        'result': None
                    })
                    continue
                
                # Apply misidentification rules
                final_results = []
                for item in filtered_results:
                    keyword = item['keyword']
                    score = item['score']
                    
                    if keyword in MISIDENTIFICATION_RULES:
                        corrected_keyword = MISIDENTIFICATION_RULES[keyword]
                        corrected_found = False
                        for other_item in filtered_results:
                            if other_item['keyword'] == corrected_keyword:
                                final_results.append({'keyword': corrected_keyword, 'score': max(score, other_item['score'])})
                                corrected_found = True
                                break
                        if not corrected_found:
                            final_results.append({'keyword': corrected_keyword, 'score': score})
                    else:
                        final_results.append(item)
                
                # Remove duplicates
                seen = set()
                unique_results = []
                for item in final_results:
                    if item['keyword'] not in seen:
                        seen.add(item['keyword'])
                        unique_results.append(item)
                
                # Sort by score
                unique_results.sort(key=lambda x: x['score'], reverse=True)
                
                # Get top result
                top_result = unique_results[0]
                name = top_result['keyword']
                confidence = top_result['score']
                
                # Determine category
                category = '未知'
                for cat, keywords in MEDICINE_CATEGORIES.items():
                    for keyword in keywords:
                        if keyword in name:
                            category = cat
                            break
                    if category != '未知':
                        break
                
                results.append({
                    'image': image_path,
                    'status': '成功',
                    'result': {
                        'name': name,
                        'category': category,
                        'confidence': confidence,
                        'candidates': [item['keyword'] for item in unique_results[:5]]
                    }
                })
            else:
                results.append({
                    'image': image_path,
                    'status': '失败',
                    'reason': 'API调用失败',
                    'result': None
                })
        
        except Exception as e:
            results.append({
                'image': image_path,
                'status': '失败',
                'reason': str(e),
                'result': None
            })
    
    return results
