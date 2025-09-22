#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

def diagnose_test_options():
    """诊断测试选项问题"""
    api_url = "http://127.0.0.1:3000/api"
    
    print("🔍 诊断测试选项问题")
    print("="*60)
    
    # 1. 检查词库数据
    print("\n1. 检查词库数据质量...")
    try:
        response = requests.get(f"{api_url}/words?grade=3&limit=10")
        result = response.json()
        
        if result.get('success') and result.get('data'):
            words = result['data']
            print(f"   ✅ 找到 {len(words)} 个三年级词汇")
            
            # 检查数据质量
            valid_words = 0
            for word in words:
                has_english = word.get('word') and word['word'].strip()
                has_chinese = word.get('chinese_meaning') and word['chinese_meaning'].strip()
                
                if has_english and has_chinese:
                    valid_words += 1
                    print(f"   ✓ {word['word']} -> {word['chinese_meaning']}")
                else:
                    print(f"   ❌ 数据不完整: {word}")
            
            print(f"   有效词汇: {valid_words}/{len(words)}")
            
            if valid_words < 4:
                print("   ⚠️  警告: 词汇数量不足，无法生成4选项测试")
                return False
                
        else:
            print("   ❌ 无法获取词库数据")
            return False
    except Exception as e:
        print(f"   ❌ 词库检查失败: {e}")
        return False
    
    # 2. 测试中译英题目生成
    print("\n2. 测试中译英题目生成...")
    try:
        test_data = {
            "user_id": 1,
            "test_type": "cn_to_en",
            "grade": 3,
            "question_count": 3
        }
        
        response = requests.post(f"{api_url}/test/generate", json=test_data)
        result = response.json()
        
        if result.get('success'):
            test = result['data']
            print(f"   ✅ 中译英测试生成成功")
            
            for i, question in enumerate(test['questions'], 1):
                print(f"\n   题目 {i}:")
                print(f"   📝 题目文本: '{question['question_text']}'")
                print(f"   🏷️  题目类型: {question['question_type']}")
                
                # 分析题目语言
                question_text = question['question_text']
                has_chinese_question = any('\u4e00' <= char <= '\u9fff' for char in question_text)
                
                print(f"   🔍 题目分析:")
                print(f"      - 包含中文字符: {has_chinese_question}")
                
                print(f"   📋 选项分析:")
                for j, option in enumerate(question['options'], 1):
                    text = option['text']
                    has_chinese_option = any('\u4e00' <= char <= '\u9fff' for char in text)
                    has_english_option = any('a' <= char.lower() <= 'z' for char in text)
                    
                    print(f"      {j}. '{text}' (中文:{has_chinese_option}, 英文:{has_english_option})")
                
                # 验证逻辑正确性
                if question['question_type'] == 'cn_to_en':
                    if not has_chinese_question:
                        print(f"   ❌ 错误: 中译英题目应该是中文，但题目是: '{question_text}'")
                    
                    english_options = 0
                    chinese_options = 0
                    for option in question['options']:
                        if any('\u4e00' <= char <= '\u9fff' for char in option['text']):
                            chinese_options += 1
                        elif any('a' <= char.lower() <= 'z' for char in option['text']):
                            english_options += 1
                    
                    print(f"   📊 选项统计: 英文选项{english_options}个, 中文选项{chinese_options}个")
                    
                    if chinese_options > 0:
                        print(f"   ❌ 错误: 中译英应该全是英文选项，但有{chinese_options}个中文选项")
                    elif english_options == len(question['options']):
                        print(f"   ✅ 正确: 中译英格式正确")
                        
        else:
            print(f"   ❌ 中译英测试生成失败: {result.get('error')}")
            return False
    except Exception as e:
        print(f"   ❌ 中译英测试失败: {e}")
        return False
    
    # 3. 测试英译中题目生成
    print("\n3. 测试英译中题目生成...")
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
                print(f"   📝 题目文本: '{question['question_text']}'")
                
                # 分析题目语言
                question_text = question['question_text']
                has_english_question = any('a' <= char.lower() <= 'z' for char in question_text)
                
                print(f"   🔍 题目分析:")
                print(f"      - 包含英文字符: {has_english_question}")
                
                print(f"   📋 选项:")
                for j, option in enumerate(question['options'], 1):
                    text = option['text']
                    print(f"      {j}. '{text}'")
                
                # 验证逻辑正确性
                if question['question_type'] == 'en_to_cn':
                    if not has_english_question:
                        print(f"   ❌ 错误: 英译中题目应该是英文，但题目是: '{question_text}'")
                    else:
                        print(f"   ✅ 正确: 英译中格式正确")
                        
        else:
            print(f"   ❌ 英译中测试生成失败: {result.get('error')}")
            
    except Exception as e:
        print(f"   ❌ 英译中测试失败: {e}")
    
    return True

def suggest_fixes():
    """建议修复方案"""
    print("\n" + "="*60)
    print("🔧 问题诊断总结和修复建议:")
    print("\n可能的问题和解决方案:")
    print("1. 词库数据不足 -> 需要添加更多测试词汇")
    print("2. 数据质量问题 -> 检查word和chinese_meaning字段")
    print("3. 前端显示问题 -> 检查模板渲染逻辑")
    print("4. 题目类型混淆 -> 验证测试生成逻辑")

if __name__ == "__main__":
    success = diagnose_test_options()
    suggest_fixes()