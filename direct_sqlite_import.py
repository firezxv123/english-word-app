#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
直接执行词库导入
"""
import sys
import os
import json
import sqlite3
from pathlib import Path

def import_words_directly():
    """直接向SQLite数据库导入词汇"""
    
    # 数据库文件路径
    db_path = 'd:/qodercode/data-dev.sqlite'
    
    if not os.path.exists(db_path):
        print(f"数据库文件不存在: {db_path}")
        return
    
    print("🚀 直接向数据库导入词汇...")
    
    # 连接数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 检查word表是否存在
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='word';")
    if not cursor.fetchone():
        print("❌ word表不存在")
        return
    
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
            print(f"📚 导入 {os.path.basename(file_path)}...")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                words_data = json.load(f)
            
            imported = 0
            for word_data in words_data:
                word = word_data['word']
                chinese_meaning = word_data['chinese_meaning']
                grade = word_data['grade']
                unit = word_data['unit']
                
                # 检查是否已存在
                cursor.execute(
                    "SELECT id FROM word WHERE word = ? AND grade = ? AND unit = ?",
                    (word, grade, unit)
                )
                
                if not cursor.fetchone():
                    # 插入新词汇
                    cursor.execute(
                        "INSERT INTO word (word, chinese_meaning, grade, unit) VALUES (?, ?, ?, ?)",
                        (word, chinese_meaning, grade, unit)
                    )
                    imported += 1
                    
                    # 显示前几个导入的词汇
                    if imported <= 3:
                        print(f"  添加: {word} -> {chinese_meaning} ({grade}年级第{unit}单元)")
            
            print(f"✅ 新增 {imported} 个词汇")
            total_imported += imported
        else:
            print(f"❌ 文件不存在: {file_path}")
    
    # 提交事务
    conn.commit()
    print(f"\n🎉 导入完成! 总计新增 {total_imported} 个词汇")
    
    # 统计结果
    print(f"\n📊 词库统计:")
    cursor.execute("SELECT COUNT(*) FROM word")
    total = cursor.fetchone()[0]
    print(f"总词汇数: {total}")
    
    for grade in [3, 4, 5, 6]:
        cursor.execute("SELECT COUNT(*) FROM word WHERE grade = ?", (grade,))
        count = cursor.fetchone()[0]
        print(f"{grade}年级: {count}个词汇")
        
        if count > 0:
            cursor.execute("SELECT DISTINCT unit FROM word WHERE grade = ? ORDER BY unit", (grade,))
            units = [row[0] for row in cursor.fetchall()]
            print(f"  单元: {units}")
    
    # 检查是否符合标准
    print(f"\n📏 标准要求检查:")
    requirements = {3: 190, 4: 210, 5: 230, 6: 165}
    
    for grade, required in requirements.items():
        cursor.execute("SELECT COUNT(*) FROM word WHERE grade = ?", (grade,))
        actual = cursor.fetchone()[0]
        percentage = (actual / required) * 100
        
        status = "✅" if actual >= required else "⚠️" if percentage >= 80 else "❌"
        print(f"{status} {grade}年级: {actual}/{required} ({percentage:.1f}%)")
    
    conn.close()

if __name__ == "__main__":
    import_words_directly()