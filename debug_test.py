#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

def debug_test_generation():
    """调试测验生成问题"""
    base_url = "http://127.0.0.1:3000"
    api_url = "http://127.0.0.1:3000/api"
    
    print("🔍 调试中译英测验选项问题")
    print("="*50)
    
    # 1. 检查词库数据
    print("\n1. 检查词库数据...")
    try:
        response = requests.get(f"{api_url}/words?grade=3&limit=5")
        result = response.json()
        
        if result.get('success') and result.get('data'):
            words = result['data']
            print(f"   找到 {len(words)} 个单词:")
            for word in words:
                print(f"   - ID:{word['id']} 英文:'{word['word']}' 中文:'{word['chinese_meaning']}'")
        else:
            print("   ❌ 无法获取词库数据")
            return
    except Exception as e:
        print(f"   ❌ 词库查询异常: {e}")
        return
    
    # 2. 生成中译英测验并检查结构
    print("\n2. 生成中译英测验...")
    test_data = {
        "user_id": 1,
        "test_type": "cn_to_en",
        "grade": 3,
        "question_count": 3
    }
    
    try:
        response = requests.post(f"{api_url}/test/generate", json=test_data)
        result = response.json()
        
        if result.get('success') and result.get('data'):
            test = result['data']
            print(f"   ✅ 测验创建成功，ID: {test['test_id'][:8]}...")
            print(f"   📝 测验类型: {test['test_type_name']}")
            print(f"   📊 题目数量: {test['total_questions']}")
            
            # 检查每个题目
            print("\n3. 检查题目结构:")
            for i, question in enumerate(test['questions'], 1):
                print(f"\n   题目 {i}:")
                print(f"   - 题目文本: '{question['question_text']}'")
                print(f"   - 题目类型: {question['question_type']}")
                print(f"   - 选项数量: {len(question['options'])}")
                
                print("   - 选项详情:")
                for j, option in enumerate(question['options'], 1):
                    print(f"     {j}. value='{option['value']}', text='{option['text']}'")
                    
                # 分析问题
                question_text = question['question_text']
                options = question['options']
                
                is_chinese_question = any('\u4e00' <= char <= '\u9fff' for char in question_text)
                english_options = [opt for opt in options if all(ord(char) < 128 for char in opt['text'])]
                chinese_options = [opt for opt in options if any('\u4e00' <= char <= '\u9fff' for char in opt['text'])]
                
                print(f"   📋 分析:")
                print(f"      题目是中文: {is_chinese_question}")
                print(f"      英文选项: {len(english_options)}")
                print(f"      中文选项: {len(chinese_options)}")
                
                if question['question_type'] == 'cn_to_en':
                    if not is_chinese_question:
                        print("   ❌ 问题: 中译英但题目不是中文!")
                    if len(english_options) != len(options):
                        print("   ❌ 问题: 中译英但选项不全是英文!")
                    if len(english_options) == len(options) and is_chinese_question:
                        print("   ✅ 正确: 中文题目 + 英文选项")
                        
        else:
            print(f"   ❌ 测验创建失败: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"   ❌ 测验生成异常: {e}")

if __name__ == "__main__":
    debug_test_generation()