"""LLM client utility functions."""

import os
import requests
import json

# GLM-4.7-Flash API配置
GLM_API_KEY = "2c7fe9eb30424df5b02d8a45ae05d5d5.LbBck8qeMiuBz5Lp"
GLM_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"


def get_llm_response(question, conversation_history=None):
    """Get response from GLM-4.7-Flash model.
    
    Args:
        question: User question
        conversation_history: List of previous messages in the conversation
    
    Returns:
        str: LLM response
    """
    try:
        headers = {
            "Authorization": f"Bearer {GLM_API_KEY}",
            "Content-Type": "application/json"
        }
        
        messages = [
            {
                "role": "system",
                "content": "你是一个中药材专家，精通中药材的各种知识，包括药材的功效、用法、禁忌等。请用专业但易懂的语言回答用户的问题。"
            }
        ]
        
        if conversation_history:
            messages.extend(conversation_history)
        
        messages.append({
            "role": "user",
            "content": question
        })
        
        data = {
            "model": "glm-4-flash",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        response = requests.post(GLM_API_URL, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                return "抱歉，无法获取回答，请稍后再试。"
        else:
            print(f"API请求失败，状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            return f"API请求失败，状态码: {response.status_code}"
    
    except requests.exceptions.Timeout:
        return "请求超时，请稍后再试。"
    except Exception as e:
        print(f"获取LLM响应时出错: {e}")
        return f"获取回答时出错: {str(e)}"
