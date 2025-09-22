#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append('/d/qodercode')

from app import create_app, db
from app.models.word import Word

def create_test_words():
    """创建测试词汇数据"""
    app = create_app()
    
    with app.app_context():
        print("📚 创建测试词汇数据")
        print("="*40)
        
        # 检查是否已有数据
        existing_count = Word.query.count()
        if existing_count > 0:
            print(f"数据库中已有 {existing_count} 个词汇")
            return
        
        # 创建测试词汇（根据2024年新版人教版PEP标准）
        test_words = [
            # 三年级上册 Unit 1
            {'word': 'hello', 'chinese_meaning': '你好', 'grade': 3, 'unit': 1},
            {'word': 'hi', 'chinese_meaning': '嗨', 'grade': 3, 'unit': 1},
            {'word': 'goodbye', 'chinese_meaning': '再见', 'grade': 3, 'unit': 1},
            {'word': 'bye', 'chinese_meaning': '拜拜', 'grade': 3, 'unit': 1},
            {'word': 'morning', 'chinese_meaning': '早上', 'grade': 3, 'unit': 1},
            
            # 三年级上册 Unit 2
            {'word': 'red', 'chinese_meaning': '红色', 'grade': 3, 'unit': 2},
            {'word': 'blue', 'chinese_meaning': '蓝色', 'grade': 3, 'unit': 2},
            {'word': 'green', 'chinese_meaning': '绿色', 'grade': 3, 'unit': 2},
            {'word': 'yellow', 'chinese_meaning': '黄色', 'grade': 3, 'unit': 2},
            {'word': 'black', 'chinese_meaning': '黑色', 'grade': 3, 'unit': 2},
            
            # 三年级上册 Unit 3
            {'word': 'cat', 'chinese_meaning': '猫', 'grade': 3, 'unit': 3},
            {'word': 'dog', 'chinese_meaning': '狗', 'grade': 3, 'unit': 3},
            {'word': 'bird', 'chinese_meaning': '鸟', 'grade': 3, 'unit': 3},
            {'word': 'fish', 'chinese_meaning': '鱼', 'grade': 3, 'unit': 3},
            {'word': 'rabbit', 'chinese_meaning': '兔子', 'grade': 3, 'unit': 3},
            
            # 四年级词汇
            {'word': 'apple', 'chinese_meaning': '苹果', 'grade': 4, 'unit': 1},
            {'word': 'banana', 'chinese_meaning': '香蕉', 'grade': 4, 'unit': 1},
            {'word': 'orange', 'chinese_meaning': '橙子', 'grade': 4, 'unit': 1},
            {'word': 'book', 'chinese_meaning': '书', 'grade': 4, 'unit': 2},
            {'word': 'pen', 'chinese_meaning': '钢笔', 'grade': 4, 'unit': 2},
            
            # 五年级词汇
            {'word': 'family', 'chinese_meaning': '家庭', 'grade': 5, 'unit': 1},
            {'word': 'father', 'chinese_meaning': '爸爸', 'grade': 5, 'unit': 1},
            {'word': 'mother', 'chinese_meaning': '妈妈', 'grade': 5, 'unit': 1},
            {'word': 'school', 'chinese_meaning': '学校', 'grade': 5, 'unit': 2},
            {'word': 'teacher', 'chinese_meaning': '老师', 'grade': 5, 'unit': 2},
        ]
        
        # 批量创建词汇
        created_count = 0
        for word_data in test_words:
            word = Word(
                word=word_data['word'],
                chinese_meaning=word_data['chinese_meaning'],
                grade=word_data['grade'],
                unit=word_data['unit'],
                phonetic='',  # 音标暂时为空
                phonics_breakdown='',
                memory_method='',
                book_version='PEP',
                audio_url=''
            )
            
            db.session.add(word)
            created_count += 1
        
        try:
            db.session.commit()
            print(f"✅ 成功创建 {created_count} 个测试词汇")
            
            # 验证数据
            print("\n📋 验证创建的数据:")
            words = Word.query.limit(5).all()
            for word in words:
                print(f"- {word.word} ({word.chinese_meaning}) - {word.grade}年级第{word.unit}单元")
                
        except Exception as e:
            db.session.rollback()
            print(f"❌ 创建失败: {e}")

if __name__ == "__main__":
    create_test_words()