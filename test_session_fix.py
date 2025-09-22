#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

def test_session_fix():
    """测试会话页面修复"""
    base_url = "http://127.0.0.1:3000"
    api_url = "http://127.0.0.1:3000/api"
    
    print("🧪 测试测验会话页面修复...")
    
    # 1. 先创建一个测验
    print("\n1. 创建测验...")
    test_data = {
        "user_id": 1,
        "test_type": "cn_to_en",
        "grade": 3,
        "unit": None,
        "question_count": 5
    }
    
    try:
        response = requests.post(f"{api_url}/test/generate", json=test_data)
        result = response.json()
        
        if response.status_code == 200 and result.get('success'):
            print("✅ 测验创建成功")
            test_id = result.get('data', {}).get('test_id')
            print(f"   测验ID: {test_id}")
            
            # 2. 测试访问会话页面
            print(f"\n2. 测试访问测验会话页面...")
            session_response = requests.get(f"{base_url}/test/session/{test_id}")
            
            if session_response.status_code == 200:
                print("✅ 测验会话页面访问成功")
                print("✅ 'test' is undefined 错误已修复")
            else:
                print(f"❌ 会话页面访问失败，状态码: {session_response.status_code}")
                print(f"   错误内容: {session_response.text[:200]}...")
                
        else:
            print(f"❌ 测验创建失败: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"❌ 测试异常: {str(e)}")

def test_user_creation():
    """确保有用户可以测试"""
    api_url = "http://127.0.0.1:3000/api"
    
    print("\n🔧 确保测试用户存在...")
    
    # 创建测试用户
    user_data = {
        "username": "测试用户",
        "grade": 3
    }
    
    try:
        response = requests.post(f"{api_url}/users", json=user_data)
        result = response.json()
        
        if response.status_code == 200 and result.get('success'):
            print("✅ 测试用户创建成功")
        elif response.status_code == 400 and "已存在" in result.get('error', ''):
            print("✅ 测试用户已存在")
        else:
            print(f"❌ 用户创建失败: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"❌ 用户创建异常: {str(e)}")

if __name__ == "__main__":
    print("🔧 测验会话UndefinedError修复验证")
    print("="*50)
    
    test_user_creation()
    test_session_fix()
    
    print("\n" + "="*50)
    print("🏁 测试完成")