#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 检查数据库中的词库数据
import os
import sys
sys.path.append('/d/qodercode')

from app import create_app, db
from app.models.word import Word

def check_word_data():
    """检查词库数据"""
    app = create_app()
    
    with app.app_context():
        print("🔍 检查数据库词库数据")
        print("="*40)
        
        # 统计总数
        total_words = Word.query.count()
        print(f"总词汇数: {total_words}")
        
        if total_words == 0:
            print("❌ 数据库中没有词汇数据!")
            print("需要先导入词库数据")
            return
        
        # 检查前5个词汇的数据结构
        words = Word.query.limit(5).all()
        print(f"\n前5个词汇示例:")
        for i, word in enumerate(words, 1):
            print(f"{i}. ID:{word.id}")
            print(f"   英文: '{word.word}'")
            print(f"   中文: '{word.chinese_meaning}'")
            print(f"   年级: {word.grade}")
            print(f"   单元: {word.unit}")
            
            # 检查数据完整性
            has_english = bool(word.word and word.word.strip())
            has_chinese = bool(word.chinese_meaning and word.chinese_meaning.strip())
            
            if not has_english:
                print(f"   ❌ 缺少英文单词")
            if not has_chinese:
                print(f"   ❌ 缺少中文含义")
            
            print()

if __name__ == "__main__":
    check_word_data()