#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append('/d/qodercode')

from app import create_app, db
from app.models.word import Word

def fix_word_data():
    """修复词库数据"""
    app = create_app()
    
    with app.app_context():
        print("🔧 修复词库数据")
        print("="*50)
        
        # 清除现有错误数据
        existing_count = Word.query.count()
        print(f"当前词汇数量: {existing_count}")
        
        if existing_count > 0:
            print("清除现有数据...")
            Word.query.delete()
            db.session.commit()
        
        # 创建正确的测试词汇数据（根据2024年新版人教版PEP标准）
        correct_words = [
            # 三年级上册基础词汇
            {'word': 'hello', 'chinese_meaning': '你好', 'grade': 3, 'unit': 1},
            {'word': 'hi', 'chinese_meaning': '嗨', 'grade': 3, 'unit': 1},
            {'word': 'goodbye', 'chinese_meaning': '再见', 'grade': 3, 'unit': 1},
            {'word': 'bye', 'chinese_meaning': '拜拜', 'grade': 3, 'unit': 1},
            {'word': 'morning', 'chinese_meaning': '早上', 'grade': 3, 'unit': 1},
            
            # 颜色词汇
            {'word': 'red', 'chinese_meaning': '红色', 'grade': 3, 'unit': 2},
            {'word': 'blue', 'chinese_meaning': '蓝色', 'grade': 3, 'unit': 2},
            {'word': 'yellow', 'chinese_meaning': '黄色', 'grade': 3, 'unit': 2},
            {'word': 'green', 'chinese_meaning': '绿色', 'grade': 3, 'unit': 2},
            {'word': 'white', 'chinese_meaning': '白色', 'grade': 3, 'unit': 2},
            {'word': 'black', 'chinese_meaning': '黑色', 'grade': 3, 'unit': 2},
            
            # 动物词汇
            {'word': 'cat', 'chinese_meaning': '猫', 'grade': 3, 'unit': 3},
            {'word': 'dog', 'chinese_meaning': '狗', 'grade': 3, 'unit': 3},
            {'word': 'bird', 'chinese_meaning': '鸟', 'grade': 3, 'unit': 3},
            {'word': 'fish', 'chinese_meaning': '鱼', 'grade': 3, 'unit': 3},
            {'word': 'rabbit', 'chinese_meaning': '兔子', 'grade': 3, 'unit': 3},
            {'word': 'tiger', 'chinese_meaning': '老虎', 'grade': 3, 'unit': 3},
            
            # 水果词汇
            {'word': 'apple', 'chinese_meaning': '苹果', 'grade': 3, 'unit': 4},
            {'word': 'banana', 'chinese_meaning': '香蕉', 'grade': 3, 'unit': 4},
            {'word': 'orange', 'chinese_meaning': '橙子', 'grade': 3, 'unit': 4},
            {'word': 'peach', 'chinese_meaning': '桃子', 'grade': 3, 'unit': 4},
            
            # 学习用品
            {'word': 'book', 'chinese_meaning': '书', 'grade': 3, 'unit': 5},
            {'word': 'pen', 'chinese_meaning': '钢笔', 'grade': 3, 'unit': 5},
            {'word': 'pencil', 'chinese_meaning': '铅笔', 'grade': 3, 'unit': 5},
            {'word': 'ruler', 'chinese_meaning': '尺子', 'grade': 3, 'unit': 5},
            {'word': 'desk', 'chinese_meaning': '桌子', 'grade': 3, 'unit': 5},
            
            # 身体部位
            {'word': 'face', 'chinese_meaning': '脸', 'grade': 3, 'unit': 6},
            {'word': 'eye', 'chinese_meaning': '眼睛', 'grade': 3, 'unit': 6},
            {'word': 'ear', 'chinese_meaning': '耳朵', 'grade': 3, 'unit': 6},
            {'word': 'nose', 'chinese_meaning': '鼻子', 'grade': 3, 'unit': 6},
            {'word': 'mouth', 'chinese_meaning': '嘴巴', 'grade': 3, 'unit': 6},
            {'word': 'arm', 'chinese_meaning': '胳膊', 'grade': 3, 'unit': 6},
            
            # 四年级词汇
            {'word': 'family', 'chinese_meaning': '家庭', 'grade': 4, 'unit': 1},
            {'word': 'father', 'chinese_meaning': '爸爸', 'grade': 4, 'unit': 1},
            {'word': 'mother', 'chinese_meaning': '妈妈', 'grade': 4, 'unit': 1},
            {'word': 'sister', 'chinese_meaning': '姐妹', 'grade': 4, 'unit': 1},
            {'word': 'brother', 'chinese_meaning': '兄弟', 'grade': 4, 'unit': 1},
            
            # 数字
            {'word': 'one', 'chinese_meaning': '一', 'grade': 4, 'unit': 2},
            {'word': 'two', 'chinese_meaning': '二', 'grade': 4, 'unit': 2},
            {'word': 'three', 'chinese_meaning': '三', 'grade': 4, 'unit': 2},
            {'word': 'four', 'chinese_meaning': '四', 'grade': 4, 'unit': 2},
            {'word': 'five', 'chinese_meaning': '五', 'grade': 4, 'unit': 2},
            
            # 形容词
            {'word': 'big', 'chinese_meaning': '大的', 'grade': 4, 'unit': 3},
            {'word': 'small', 'chinese_meaning': '小的', 'grade': 4, 'unit': 3},
            {'word': 'tall', 'chinese_meaning': '高的', 'grade': 4, 'unit': 3},
            {'word': 'short', 'chinese_meaning': '矮的', 'grade': 4, 'unit': 3},
            {'word': 'old', 'chinese_meaning': '老的', 'grade': 4, 'unit': 3},
            {'word': 'new', 'chinese_meaning': '新的', 'grade': 4, 'unit': 3},
            
            # 食物
            {'word': 'cake', 'chinese_meaning': '蛋糕', 'grade': 4, 'unit': 4},
            {'word': 'bread', 'chinese_meaning': '面包', 'grade': 4, 'unit': 4},
            {'word': 'milk', 'chinese_meaning': '牛奶', 'grade': 4, 'unit': 4},
            {'word': 'water', 'chinese_meaning': '水', 'grade': 4, 'unit': 4},
            {'word': 'chicken', 'chinese_meaning': '鸡肉', 'grade': 4, 'unit': 4},
            
            # 体育用品
            {'word': 'ball', 'chinese_meaning': '球', 'grade': 4, 'unit': 5},
            {'word': 'football', 'chinese_meaning': '足球', 'grade': 4, 'unit': 5},
            {'word': 'basketball', 'chinese_meaning': '篮球', 'grade': 4, 'unit': 5},
        ]
        
        # 批量创建词汇
        created_count = 0
        for word_data in correct_words:
            word = Word(
                word=word_data['word'],
                chinese_meaning=word_data['chinese_meaning'],
                grade=word_data['grade'],
                unit=word_data['unit'],
                phonetic='',  # 音标可以后续添加
                phonics_breakdown='',
                memory_method='',
                book_version='PEP',
                audio_url=''
            )
            
            db.session.add(word)
            created_count += 1
        
        try:
            db.session.commit()
            print(f"✅ 成功创建 {created_count} 个正确的词汇")
            
            # 验证修复结果
            print("\n📋 验证修复结果:")
            print("前10个词汇:")
            words = Word.query.limit(10).all()
            for word in words:
                print(f"  {word.word} -> {word.chinese_meaning} ({word.grade}年级第{word.unit}单元)")
                
        except Exception as e:
            db.session.rollback()
            print(f"❌ 创建失败: {e}")

if __name__ == "__main__":
    fix_word_data()