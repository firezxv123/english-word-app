#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
简单的数据修复脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.word import Word

def fix_word_units():
    """修复词库单元数据"""
    app = create_app()
    
    with app.app_context():
        print("开始修复词库单元数据...")
        
        # 查找单元号大于12的单词
        words_to_fix = Word.query.filter(Word.unit > 12).all()
        
        print(f"发现{len(words_to_fix)}个需要修复的单词")
        
        fixed_count = 0
        for word in words_to_fix:
            print(f"修复单词: {word.word} (年级:{word.grade}, 单元:{word.unit} -> 12)")
            word.unit = 12  # 调整到最大单元
            fixed_count += 1
        
        # 查找六年级单元号大于10的单词
        grade6_words_to_fix = Word.query.filter(Word.grade == 6, Word.unit > 10).all()
        
        for word in grade6_words_to_fix:
            print(f"修复六年级单词: {word.word} (单元:{word.unit} -> 10)")
            word.unit = 10
            fixed_count += 1
        
        # 提交更改
        try:
            db.session.commit()
            print(f"成功修复了{fixed_count}个单词的单元数据")
        except Exception as e:
            db.session.rollback()
            print(f"修复失败: {str(e)}")

if __name__ == '__main__':
    fix_word_units()