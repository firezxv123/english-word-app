#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app import create_app, db
from app.models.word import Word

def analyze_word_database():
    """分析当前词库数据"""
    app = create_app()
    
    with app.app_context():
        print("📊 当前词库分析报告")
        print("="*50)
        
        # 总体统计
        total_words = Word.query.count()
        print(f"总词汇数: {total_words}")
        
        # 各年级详细统计
        for grade in [3, 4, 5, 6]:
            print(f"\n📚 {grade}年级详细分析:")
            grade_words = Word.query.filter_by(grade=grade).all()
            print(f"  总数: {len(grade_words)}个词汇")
            
            if grade_words:
                # 按单元统计
                units = {}
                for word in grade_words:
                    unit = word.unit or 0
                    if unit not in units:
                        units[unit] = []
                    units[unit].append(word)
                
                print(f"  单元分布:")
                for unit in sorted(units.keys()):
                    words_in_unit = units[unit]
                    print(f"    第{unit}单元: {len(words_in_unit)}个词汇")
                    
                    # 显示前3个词汇示例
                    examples = [f"{w.word}({w.chinese_meaning})" for w in words_in_unit[:3]]
                    if len(words_in_unit) > 3:
                        examples.append("...")
                    print(f"      示例: {', '.join(examples)}")
            else:
                print("  ❌ 暂无词汇数据")
        
        # 标准对比
        print(f"\n📏 与教材标准对比:")
        standards = {
            3: {"required": 190, "description": "三年级上下册"},
            4: {"required": 210, "description": "四年级上下册"}, 
            5: {"required": 230, "description": "五年级上下册"},
            6: {"required": 165, "description": "六年级上下册"}
        }
        
        for grade, info in standards.items():
            actual = Word.query.filter_by(grade=grade).count()
            required = info["required"]
            percentage = (actual / required) * 100
            
            status = "✅" if actual >= required else "⚠️" if percentage >= 50 else "❌"
            print(f"  {status} {grade}年级: {actual}/{required} ({percentage:.1f}%) - {info['description']}")

if __name__ == "__main__":
    analyze_word_database()