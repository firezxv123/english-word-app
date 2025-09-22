#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
页面测试脚本 - 验证所有页面是否可以正常访问
"""

import requests
import sys
import time

# 应用基础URL
BASE_URL = 'http://127.0.0.1:3000'

def test_page(url, description, method='GET', data=None):
    """测试单个页面"""
    try:
        full_url = f"{BASE_URL}{url}"
        print(f"测试 {description}: {full_url}")
        
        if method == 'GET':
            response = requests.get(full_url, timeout=10)
        elif method == 'POST':
            response = requests.post(full_url, json=data, timeout=10)
        
        if response.status_code == 200:
            print(f"  ✅ 成功 - 状态码: {response.status_code}")
            return True
        else:
            print(f"  ❌ 失败 - 状态码: {response.status_code}")
            if response.status_code >= 400:
                print(f"     错误信息: {response.text[:200]}...")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"  ❌ 连接失败 - 应用可能未运行")
        return False
    except Exception as e:
        print(f"  ❌ 错误: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试所有页面...")
    print(f"测试目标: {BASE_URL}")
    print("-" * 50)
    
    # 测试用例列表
    test_cases = [
        # 基础页面
        ('/', '首页'),
        ('/user/select', '用户选择页面'),
        ('/user/create', '创建用户页面'),
        
        # 带参数的页面（使用空参数测试）
        ('/?user_id=', '首页带空用户ID'),
        ('/?user_id=1', '首页带用户ID'),
        ('/word/list?grade=', '词库浏览带空年级'),
        ('/word/list?grade=3', '词库浏览三年级'),
        ('/word/list?grade=3&unit=', '词库浏览带空单元'),
        ('/word/list?grade=3&unit=1', '词库浏览三年级第一单元'),
        
        # API测试
        ('/api/words', 'API - 获取词库'),
        ('/api/words?grade=', 'API - 获取词库带空年级'),
        ('/api/words?grade=3', 'API - 获取三年级词库'),
        ('/api/words?grade=3&unit=', 'API - 获取词库带空单元'),
        ('/api/words?grade=3&unit=1', 'API - 获取三年级第一单元词库'),
        ('/api/words/grades', 'API - 获取年级列表'),
        ('/api/words/units/3', 'API - 获取三年级单元列表'),
        ('/api/words/statistics', 'API - 获取词库统计'),
        
        # 用户相关API
        ('/api/users', 'API - 获取用户列表'),
        
        # 管理页面
        ('/admin/logs', '管理员日志页面'),
        ('/admin/system/info', '系统信息页面'),
        
        # 导出页面
        ('/export', '数据导出页面'),
        
        # 缓存API
        ('/api/cache/stats', 'API - 缓存统计'),
        ('/api/cache/health', 'API - 缓存健康检查'),
    ]
    
    success_count = 0
    total_count = len(test_cases)
    
    for url, description in test_cases:
        if test_page(url, description):
            success_count += 1
        time.sleep(0.5)  # 避免请求过快
        print()
    
    print("-" * 50)
    print(f"📊 测试结果: {success_count}/{total_count} 成功")
    
    if success_count == total_count:
        print("🎉 所有页面测试通过！")
        return True
    else:
        print("⚠️  有部分页面测试失败，请检查应用状态")
        return False

def test_parameter_handling():
    """专门测试参数处理"""
    print("\n🔧 测试参数处理...")
    print("-" * 30)
    
    # 测试各种边界情况的参数
    test_params = [
        ('', '空字符串'),
        ('abc', '非数字字符串'),
        ('-1', '负数'),
        ('0', '零'),
        ('999', '大数字'),
    ]
    
    for param_value, description in test_params:
        url = f"/api/words?grade={param_value}&unit={param_value}"
        print(f"测试参数 {description} ({param_value}): ", end='')
        
        try:
            response = requests.get(f"{BASE_URL}{url}", timeout=5)
            if response.status_code == 200:
                print("✅ 正常")
            else:
                print(f"❌ 状态码: {response.status_code}")
        except Exception as e:
            print(f"❌ 错误: {str(e)}")

if __name__ == '__main__':
    print("=" * 60)
    print("🧪 小学英语单词复习应用 - 页面测试工具")
    print("=" * 60)
    
    # 主页面测试
    success = main()
    
    # 参数处理测试
    test_parameter_handling()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ 测试完成 - 应用运行正常")
        sys.exit(0)
    else:
        print("❌ 测试完成 - 发现问题")
        sys.exit(1)