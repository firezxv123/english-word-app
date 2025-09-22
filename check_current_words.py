#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 检查当前词库数据
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app import create_app, db
from app.models.word import Word

def check_words():
    """检查当前词库数据"""
    app = create_app()
    
    with app.app_context():
        print("🔍 检查当前词库数据")
        print("="*50)
        
        # 统计总数
        total_words = Word.query.count()
        print(f"总词汇数: {total_words}")
        
        if total_words == 0:
            print("❌ 数据库中没有词汇数据!")
            return
        
        print(f"\n📊 各年级词汇统计:")
        for grade in [3, 4, 5, 6]:
            count = Word.query.filter_by(grade=grade).count()
            print(f"{grade}年级: {count}个词汇")
            
            if count > 0:
                # 获取该年级的单元分布
                units = db.session.query(Word.unit).filter_by(grade=grade).distinct().all()
                unit_list = sorted([u[0] for u in units if u[0] is not None])
                print(f"  单元分布: {unit_list}")
                
                # 显示每个单元的词汇数
                for unit in unit_list:
                    unit_count = Word.query.filter_by(grade=grade, unit=unit).count()
                    print(f"    第{unit}单元: {unit_count}个词汇")
        
        print(f"\n📝 词汇数据示例 (前3个):")
        sample_words = Word.query.limit(3).all()
        for i, word in enumerate(sample_words, 1):
            print(f"{i}. {word.word} -> {word.chinese_meaning} ({word.grade}年级第{word.unit}单元)")

if __name__ == "__main__":
    check_words()