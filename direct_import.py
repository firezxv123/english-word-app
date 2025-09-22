#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import json

# 添加项目路径
sys.path.insert(0, 'd:/qodercode')

# 直接导入
from app import create_app, db
from app.models.word import Word

app = create_app()

with app.app_context():
    print("开始导入词汇...")
    
    # 要导入的文件列表
    files = [
        'd:/qodercode/grade3_words_part1.json',
        'd:/qodercode/grade3_words_part2.json', 
        'd:/qodercode/grade4_words.json',
        'd:/qodercode/grade5_words.json',
        'd:/qodercode/grade6_words.json'
    ]
    
    total_imported = 0
    
    for file_path in files:
        if os.path.exists(file_path):
            print(f"导入 {os.path.basename(file_path)}...")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                words_data = json.load(f)
            
            imported = 0
            for word_data in words_data:
                # 检查是否已存在
                existing = Word.query.filter_by(
                    word=word_data['word'], 
                    grade=word_data['grade'], 
                    unit=word_data['unit']
                ).first()
                
                if not existing:
                    new_word = Word(
                        word=word_data['word'],
                        chinese_meaning=word_data['chinese_meaning'],
                        grade=word_data['grade'],
                        unit=word_data['unit']
                    )
                    db.session.add(new_word)
                    imported += 1
                    if imported <= 3:  # 只显示前3个
                        print(f"  添加: {word_data['word']} -> {word_data['chinese_meaning']}")
            
            print(f"新增 {imported} 个词汇")
            total_imported += imported
    
    db.session.commit()
    print(f"\n导入完成! 总计新增 {total_imported} 个词汇")
    
    # 统计结果
    print("\n词库统计:")
    for grade in [3, 4, 5, 6]:
        count = Word.query.filter_by(grade=grade).count()
        print(f"{grade}年级: {count}个词汇")