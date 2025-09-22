#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
快速验证修复效果的测试脚本
"""

import requests
import json

BASE_URL = 'http://127.0.0.1:3000'

def test_endpoint(url, description):
    """测试单个端点"""
    try:
        full_url = f"{BASE_URL}{url}"
        response = requests.get(full_url, timeout=5)
        
        status = "✅ 正常" if response.status_code == 200 else f"❌ {response.status_code}"
        print(f"{description}: {status}")
        
        # 如果是500错误，尝试获取错误信息
        if response.status_code == 500:
            try:
                error_data = response.json()
                print(f"   错误: {error_data.get('error', '未知错误')}")
            except:
                print(f"   服务器内部错误")
                
        return response.status_code == 200
    except Exception as e:
        print(f"{description}: ❌ 连接错误 - {str(e)}")
        return False

def main():
    print("🔍 快速验证修复效果...")
    print("=" * 40)
    
    # 核心端点测试
    tests = [
        ('/', '首页'),
        ('/test/1', '测验主页'),
        ('/test/1/create', '创建测验页面'),
        ('/test/1/history', '测验历史页面'),
        ('/api/users', 'API - 用户列表'),
        ('/api/words', 'API - 单词列表'),
        ('/api/cache/stats', 'API - 缓存统计'),
        ('/maintenance', '维护页面'),
    ]
    
    success_count = 0
    for url, desc in tests:
        if test_endpoint(url, desc):
            success_count += 1
    
    print("=" * 40)
    print(f"📊 测试结果: {success_count}/{len(tests)} 通过")
    
    if success_count == len(tests):
        print("🎉 所有测试通过！ValueError问题已解决！")
    else:
        print("⚠️  仍有问题需要解决")

if __name__ == '__main__':
    main()