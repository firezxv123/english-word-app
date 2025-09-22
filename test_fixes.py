#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

def test_api_endpoints():
    """测试所有API端点的参数处理"""
    base_url = "http://127.0.0.1:3000/api"
    
    print("🧪 开始测试API参数安全处理...")
    
    # 测试1: 测试生成测验API（可能的ValueError来源）
    test_data = {
        "user_id": 1,
        "test_type": "cn_to_en",
        "grade": "",  # 空字符串
        "unit": "",   # 空字符串
        "question_count": ""  # 空字符串
    }
    
    print("\n1. 测试测验生成API (空字符串参数)")
    try:
        response = requests.post(f"{base_url}/test/generate", json=test_data)
        result = response.json()
        if response.status_code == 200 and result.get('success'):
            print("✅ 测验生成API - 空字符串参数处理正常")
        else:
            print(f"❌ 测验生成API失败: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"❌ 测验生成API异常: {str(e)}")
    
    # 测试2: 测试正常参数
    test_data_normal = {
        "user_id": 1,
        "test_type": "cn_to_en",
        "grade": 3,
        "unit": 1,
        "question_count": 10
    }
    
    print("\n2. 测试测验生成API (正常参数)")
    try:
        response = requests.post(f"{base_url}/test/generate", json=test_data_normal)
        result = response.json()
        if response.status_code == 200 and result.get('success'):
            print("✅ 测验生成API - 正常参数处理正常")
            test_id = result.get('data', {}).get('test_id')
            if test_id:
                print(f"   测验ID: {test_id}")
        else:
            print(f"❌ 测验生成API失败: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"❌ 测验生成API异常: {str(e)}")
    
    # 测试3: 测试用户测验历史API
    print("\n3. 测试用户测验历史API")
    try:
        response = requests.get(f"{base_url}/test/history/1?limit=")  # 空字符串limit
        result = response.json()
        if response.status_code == 200 and result.get('success'):
            print("✅ 测验历史API - 空limit参数处理正常")
        else:
            print(f"❌ 测验历史API失败: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"❌ 测验历史API异常: {str(e)}")
    
    # 测试4: 测试词库API
    print("\n4. 测试词库API")
    try:
        response = requests.get(f"{base_url}/words?grade=&unit=&limit=")  # 所有参数为空
        result = response.json()
        if response.status_code == 200 and result.get('success'):
            print("✅ 词库API - 空参数处理正常")
        else:
            print(f"❌ 词库API失败: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"❌ 词库API异常: {str(e)}")
    
    # 测试5: 测试学习进度API
    print("\n5. 测试学习进度API")
    try:
        response = requests.get(f"{base_url}/study/progress/1?grade=&unit=")  # 空参数
        result = response.json()
        if response.status_code == 200 and result.get('success'):
            print("✅ 学习进度API - 空参数处理正常")
        else:
            print(f"❌ 学习进度API失败: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"❌ 学习进度API异常: {str(e)}")

def test_web_pages():
    """测试Web页面"""
    base_url = "http://127.0.0.1:3000"
    
    print("\n\n🌐 开始测试Web页面...")
    
    # 测试页面列表
    pages = [
        "/",
        "/users",
        "/test/1",
        "/test/1/create",
        "/test/1/history",
        "/study/1",
        "/study/1/progress",
        "/maintenance"
    ]
    
    for page in pages:
        try:
            response = requests.get(f"{base_url}{page}")
            if response.status_code == 200:
                print(f"✅ 页面 {page} - 正常访问")
            else:
                print(f"❌ 页面 {page} - 状态码: {response.status_code}")
        except Exception as e:
            print(f"❌ 页面 {page} - 异常: {str(e)}")

if __name__ == "__main__":
    print("🔧 参数处理修复验证测试")
    print("="*50)
    
    test_api_endpoints()
    test_web_pages()
    
    print("\n" + "="*50)
    print("🏁 测试完成")
    print("\n💡 如果所有测试都通过，说明ValueError问题已修复")
    print("💡 如果仍有问题，请查看终端日志获取详细错误信息")