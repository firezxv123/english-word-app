#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import time

def test_cn_to_en_options():
    """测试中译英选项问题"""
    api_url = "http://127.0.0.1:3000/api"
    
    print("🧪 测试中译英选项问题修复")
    print("="*50)
    
    # 1. 创建测试用户
    print("1. 确保测试用户存在...")
    try:
        user_response = requests.post(f"{api_url}/users", json={"username": "测试学生", "grade": 3})
        print("✅ 用户准备完成")
    except:
        pass  # 用户可能已存在
    
    # 2. 检查词库
    print("\n2. 检查词库数据...")
    try:
        words_response = requests.get(f"{api_url}/words?grade=3&limit=10")
        words_result = words_response.json()
        
        if words_result.get('success') and words_result.get('data'):
            words = words_result['data']
            print(f"   ✅ 找到 {len(words)} 个词汇")
            
            # 显示前3个词汇
            for i, word in enumerate(words[:3], 1):
                print(f"   {i}. '{word['word']}' -> '{word['chinese_meaning']}'")
        else:
            print("   ❌ 词库数据为空，需要先创建数据")
            return False
    except Exception as e:
        print(f"   ❌ 词库查询失败: {e}")
        return False
    
    # 3. 生成中译英测验
    print("\n3. 生成中译英测验...")
    test_data = {
        "user_id": 1,
        "test_type": "cn_to_en",  # 重点：中译英
        "grade": 3,
        "question_count": 5
    }
    
    try:
        response = requests.post(f"{api_url}/test/generate", json=test_data, timeout=10)
        result = response.json()
        
        if response.status_code == 200 and result.get('success'):
            print("✅ 测验生成成功")
            test_info = result['data']
            
            print(f"   测验类型: {test_info['test_type_name']}")
            print(f"   题目数量: {test_info['total_questions']}")
            
            # 4. 分析题目格式
            print(f"\n4. 分析题目格式:")
            for i, question in enumerate(test_info['questions'], 1):
                print(f"\n   题目 {i}:")
                print(f"   题目: {question['question_text']}")
                print(f"   类型: {question['question_type']}")
                print(f"   选项:")
                
                for j, option in enumerate(question['options'], 1):
                    print(f"     {j}. {option['text']}")
                
                # 验证格式正确性
                question_text = question['question_text']
                options = [opt['text'] for opt in question['options']]
                
                # 检查题目是否为中文
                has_chinese_chars = any('\u4e00' <= char <= '\u9fff' for char in question_text)
                
                # 检查选项是否为英文
                all_english_options = all(
                    all(ord(char) < 128 or char.isspace() for char in opt) 
                    for opt in options
                )
                
                if question['question_type'] == 'cn_to_en':
                    if has_chinese_chars and all_english_options:
                        print(f"   ✅ 格式正确: 中文题目 + 英文选项")
                    elif not has_chinese_chars:
                        print(f"   ❌ 问题: 题目不是中文")
                    elif not all_english_options:
                        print(f"   ❌ 问题: 选项不全是英文")
                        # 分析具体哪个选项有问题
                        for k, opt in enumerate(options, 1):
                            is_english = all(ord(char) < 128 or char.isspace() for char in opt)
                            if not is_english:
                                print(f"      选项{k}有中文字符: '{opt}'")
            
            return True
            
        else:
            print(f"❌ 测验生成失败: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ 测验生成异常: {e}")
        return False

if __name__ == "__main__":
    success = test_cn_to_en_options()
    if success:
        print("\n🎉 测试完成，请检查输出结果")
    else:
        print("\n❌ 测试失败，需要进一步排查问题")