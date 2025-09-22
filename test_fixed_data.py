#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

def test_fixed_data():
    """测试修复后的数据"""
    api_url = "http://127.0.0.1:3000/api"
    
    print("🧪 测试修复后的词库数据和测验功能")
    print("="*60)
    
    # 1. 直接通过API创建正确的词汇（如果数据库为空）
    print("1. 确保有正确的测试数据...")
    try:
        # 创建一些测试词汇
        test_words = [
            {"word": "hello", "chinese_meaning": "你好", "grade": 3, "unit": 1},
            {"word": "apple", "chinese_meaning": "苹果", "grade": 3, "unit": 1},
            {"word": "cat", "chinese_meaning": "猫", "grade": 3, "unit": 1},
            {"word": "red", "chinese_meaning": "红色", "grade": 3, "unit": 1},
            {"word": "book", "chinese_meaning": "书", "grade": 3, "unit": 1},
            {"word": "dog", "chinese_meaning": "狗", "grade": 3, "unit": 1},
        ]
        
        for word_data in test_words:
            try:
                response = requests.post(f"{api_url}/words", json=word_data)
                # 忽略"已存在"错误
            except:
                pass
        
        print("   ✅ 测试词汇准备完成")
    except Exception as e:
        print(f"   ⚠️  词汇创建警告: {e}")
    
    # 2. 检查词库数据质量
    print("\n2. 检查词库数据质量...")
    try:
        response = requests.get(f"{api_url}/words?grade=3&limit=6")
        result = response.json()
        
        if result.get('success') and result.get('data'):
            words = result['data']
            print(f"   ✅ 找到 {len(words)} 个词汇")
            
            for word in words:
                print(f"   📝 {word['word']} -> {word['chinese_meaning']}")
                
                # 检查数据质量
                if "的中文意思" in word['chinese_meaning']:
                    print(f"   ❌ 发现问题数据: {word['chinese_meaning']}")
                else:
                    print(f"   ✅ 数据正确")
        else:
            print(f"   ❌ 无法获取词库: {result}")
            return False
    except Exception as e:
        print(f"   ❌ 词库检查失败: {e}")
        return False
    
    # 3. 测试中译英
    print("\n3. 测试中译英功能...")
    try:
        test_data = {
            "user_id": 1,
            "test_type": "cn_to_en",
            "grade": 3,
            "question_count": 2
        }
        
        response = requests.post(f"{api_url}/test/generate", json=test_data)
        result = response.json()
        
        if result.get('success'):
            test = result['data']
            print(f"   ✅ 中译英测试生成成功")
            
            for i, question in enumerate(test['questions'], 1):
                print(f"\n   题目 {i}:")
                print(f"   🔍 题目: {question['question_text']}")
                print(f"   📋 选项:")
                for j, option in enumerate(question['options'], 1):
                    print(f"      {j}. {option['text']}")
                    
                # 验证格式
                if any('\u4e00' <= char <= '\u9fff' for char in question['question_text']):
                    all_english = all(
                        all(ord(char) < 128 or char.isspace() for char in opt['text'])
                        for opt in question['options']
                    )
                    if all_english:
                        print(f"   ✅ 格式正确: 中文题目 + 英文选项")
                    else:
                        print(f"   ❌ 格式错误: 选项不全是英文")
        else:
            print(f"   ❌ 测试生成失败: {result.get('error')}")
            
    except Exception as e:
        print(f"   ❌ 中译英测试失败: {e}")
    
    # 4. 测试英译中
    print("\n4. 测试英译中功能...")
    try:
        test_data = {
            "user_id": 1,
            "test_type": "en_to_cn",
            "grade": 3,
            "question_count": 2
        }
        
        response = requests.post(f"{api_url}/test/generate", json=test_data)
        result = response.json()
        
        if result.get('success'):
            test = result['data']
            print(f"   ✅ 英译中测试生成成功")
            
            for i, question in enumerate(test['questions'], 1):
                print(f"\n   题目 {i}:")
                print(f"   🔍 题目: {question['question_text']}")
                print(f"   📋 选项:")
                for j, option in enumerate(question['options'], 1):
                    print(f"      {j}. {option['text']}")
                    
                # 验证格式
                if any('a' <= char.lower() <= 'z' for char in question['question_text']):
                    all_chinese = all(
                        any('\u4e00' <= char <= '\u9fff' for char in opt['text'])
                        for opt in question['options']
                    )
                    if all_chinese:
                        print(f"   ✅ 格式正确: 英文题目 + 中文选项")
                    else:
                        print(f"   ❌ 格式错误: 选项不全是中文")
        else:
            print(f"   ❌ 测试生成失败: {result.get('error')}")
            
    except Exception as e:
        print(f"   ❌ 英译中测试失败: {e}")
    
    print(f"\n{'='*60}")
    print("🎯 总结:")
    print("现在应该可以正常看到:")
    print("• 中译英: 中文题目(如'苹果') + 英文选项(如 apple, book, cat, dog)")  
    print("• 英译中: 英文题目(如'apple') + 中文选项(如 苹果, 书, 猫, 狗)")
    print("\n如果还有问题，请检查浏览器缓存或重新加载页面!")

if __name__ == "__main__":
    test_fixed_data()