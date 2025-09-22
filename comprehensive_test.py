#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
全面的页面功能测试脚本
测试所有页面和API是否正常工作
"""

import requests
import time
import json
from urllib.parse import urljoin

BASE_URL = 'http://127.0.0.1:3000'

def test_page(url, description, expected_status=200):
    """测试单个页面"""
    try:
        full_url = urljoin(BASE_URL, url)
        response = requests.get(full_url, timeout=10)
        
        if response.status_code == expected_status:
            print(f"✅ {description}: {response.status_code}")
            return True
        else:
            print(f"❌ {description}: 期望 {expected_status}, 实际 {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {description}: 连接错误 - {str(e)}")
        return False

def test_api_post(url, data, description):
    """测试POST API"""
    try:
        full_url = urljoin(BASE_URL, url)
        response = requests.post(full_url, json=data, timeout=10)
        
        if 200 <= response.status_code <= 201:
            print(f"✅ {description}: {response.status_code}")
            return True, response.json()
        else:
            print(f"❌ {description}: 状态码 {response.status_code}")
            try:
                error_data = response.json()
                print(f"   错误详情: {error_data.get('error', '未知错误')}")
            except:
                pass
            return False, None
    except requests.exceptions.RequestException as e:
        print(f"❌ {description}: 连接错误 - {str(e)}")
        return False, None

def create_test_user():
    """创建测试用户"""
    print("\n🔧 创建测试用户...")
    user_data = {
        'username': f'测试用户_{int(time.time())}',
        'grade': 3
    }
    
    success, result = test_api_post('/api/users', user_data, '创建测试用户')
    if success and result:
        user_id = result.get('data', {}).get('id')
        print(f"   用户ID: {user_id}")
        return user_id
    return None

def test_parameter_edge_cases():
    """测试参数边界情况"""
    print("\n🔧 测试参数边界情况...")
    print("-" * 30)
    
    # 测试不同的参数值
    test_urls = [
        '/test/1/history?limit=',  # 空字符串
        '/test/1/history?limit=abc',  # 非数字
        '/test/1/history?limit=0',  # 零
        '/test/1/history?limit=999',  # 大数字
    ]
    
    for url in test_urls:
        test_page(url, f'参数测试: {url}', expected_status=200)

def run_comprehensive_tests():
    """运行全面测试"""
    print("🚀 开始全面页面测试...")
    print("=" * 50)
    
    # 基础页面测试
    print("\n📄 基础页面测试")
    print("-" * 20)
    
    basic_pages = [
        ('/', '主页'),
        ('/select_user', '选择用户页面'),
        ('/maintenance', '维护页面'),
    ]
    
    success_count = 0
    total_tests = 0
    
    for url, desc in basic_pages:
        if test_page(url, desc):
            success_count += 1
        total_tests += 1
        time.sleep(0.2)
    
    # 创建测试用户用于后续测试
    test_user_id = create_test_user()
    
    if test_user_id:
        # 用户相关页面测试
        print("\n👤 用户相关页面测试")
        print("-" * 20)
        
        user_pages = [
            (f'/study/{test_user_id}', '学习主页'),
            (f'/study/{test_user_id}/progress', '学习进度'),
            (f'/test/{test_user_id}', '测验主页'),
            (f'/test/{test_user_id}/create', '创建测验'),
            (f'/test/{test_user_id}/history', '测验历史'),
            (f'/test/{test_user_id}/statistics', '测验统计'),
        ]
        
        for url, desc in user_pages:
            if test_page(url, desc):
                success_count += 1
            total_tests += 1
            time.sleep(0.2)
    
    # API测试
    print("\n🔌 API功能测试")
    print("-" * 20)
    
    api_tests = [
        ('/api/words', '获取单词列表'),
        ('/api/users', '获取用户列表'),
        ('/api/cache/stats', '缓存统计'),
        ('/api/cache/health', '缓存健康检查'),
    ]
    
    for url, desc in api_tests:
        if test_page(url, desc):
            success_count += 1
        total_tests += 1
        time.sleep(0.2)
    
    # 参数边界测试
    test_parameter_edge_cases()
    
    # 管理页面测试
    print("\n🛠️ 管理功能测试")
    print("-" * 20)
    
    admin_pages = [
        ('/admin/logs', '管理员日志'),
        ('/admin/system/info', '系统信息'),
        ('/export', '数据导出'),
    ]
    
    for url, desc in admin_pages:
        if test_page(url, desc):
            success_count += 1
        total_tests += 1
        time.sleep(0.2)
    
    # 测试测验流程（如果有测试用户）
    if test_user_id:
        print("\n🧪 测验流程测试")
        print("-" * 20)
        
        # 测试生成测验
        test_data = {
            'user_id': test_user_id,
            'test_type': 'cn_to_en',
            'grade': 3,
            'unit': 1,
            'question_count': 5
        }
        
        success, result = test_api_post('/api/test/generate', test_data, '生成测验')
        if success:
            success_count += 1
        total_tests += 1
    
    # 维护功能测试
    print("\n🔧 维护功能测试")
    print("-" * 20)
    
    maintenance_tests = [
        ('/api/maintenance/check-system', '系统检查'),
        ('/api/maintenance/cache-clear', '清除缓存'),
    ]
    
    for url, desc in maintenance_tests:
        if test_page(url, desc):
            success_count += 1
        total_tests += 1
        time.sleep(0.2)
    
    # 输出测试结果
    print("\n" + "=" * 50)
    print(f"📊 测试结果总结: {success_count}/{total_tests} 通过")
    
    if success_count == total_tests:
        print("🎉 所有测试通过！应用运行正常。")
        return True
    else:
        failure_rate = ((total_tests - success_count) / total_tests) * 100
        print(f"⚠️  {failure_rate:.1f}% 的测试失败，需要检查问题。")
        return False

def test_specific_error_cases():
    """测试特定错误情况"""
    print("\n🐛 特定错误情况测试")
    print("-" * 25)
    
    # 测试导致ValueError的具体情况
    error_test_urls = [
        # 测试空参数情况
        '/test/1?grade=&unit=',
        '/study/1?grade=&unit=',
        '/api/words?grade=&unit=',
        # 测试非法参数
        '/test/999/create',  # 不存在的用户
        '/test/1/history?limit=abc',  # 非数字限制
    ]
    
    print("测试可能导致ValueError的URL:")
    for url in error_test_urls:
        # 对于这些测试，我们期望它们能正常处理而不是崩溃
        status = test_page(url, f'错误处理测试: {url}', expected_status=200)
        if not status:
            # 如果返回404或其他状态码也是可接受的，只要不是500
            try:
                response = requests.get(urljoin(BASE_URL, url), timeout=5)
                if response.status_code in [200, 404]:
                    print(f"   ✅ 正确处理了错误情况 (状态码: {response.status_code})")
                elif response.status_code == 500:
                    print(f"   ❌ 服务器内部错误，需要修复!")
                else:
                    print(f"   ⚠️  返回状态码: {response.status_code}")
            except:
                print(f"   ❌ 连接失败")
        time.sleep(0.3)

if __name__ == '__main__':
    try:
        # 检查服务器是否运行
        test_page('/', '检查服务器状态')
        
        # 运行全面测试
        success = run_comprehensive_tests()
        
        # 运行错误情况测试
        test_specific_error_cases()
        
        if success:
            print("\n✅ 应用测试完成，所有功能正常！")
        else:
            print("\n⚠️  测试发现问题，请查看上述报告。")
            
    except KeyboardInterrupt:
        print("\n\n⏹️  测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {str(e)}")