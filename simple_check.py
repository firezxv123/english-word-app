#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 简单的词库状态检查
import os
import sys
import sqlite3

def check_database_status():
    """检查数据库词库状态"""
    db_path = 'd:/qodercode/data-dev.sqlite'
    
    if not os.path.exists(db_path):
        print("❌ 数据库文件不存在!")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查words表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='words';")
        if not cursor.fetchone():
            print("❌ words表不存在!")
            return
        
        # 统计各年级词汇数量
        print("📊 词库统计:")
        for grade in [3, 4, 5, 6]:
            cursor.execute("SELECT COUNT(*) FROM words WHERE grade = ?", (grade,))
            count = cursor.fetchone()[0]
            print(f"  {grade}年级: {count} 个词汇")
        
        # 统计总数
        cursor.execute("SELECT COUNT(*) FROM words")
        total = cursor.fetchone()[0]
        print(f"  总计: {total} 个词汇")
        
        # 检查6年级词汇样例
        print(f"\n📖 六年级词汇样例:")
        cursor.execute("SELECT word, chinese_meaning, unit FROM words WHERE grade = 6 LIMIT 10")
        for word, meaning, unit in cursor.fetchall():
            print(f"  {word} -> {meaning} (第{unit}单元)")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ 检查数据库时出错: {str(e)}")

if __name__ == "__main__":
    check_database_status()