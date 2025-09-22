#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
人教版PEP小学英语词库导入脚本
根据2024年新版教材标准补充完整的3-6年级词汇
"""

import sys
import os
import json
sys.path.insert(0, os.path.abspath('.'))

from app import create_app, db
from app.models.word import Word

def import_words_from_json(json_file):
    """从JSON文件导入词汇"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            words_data = json.load(f)
        
        imported_count = 0
        updated_count = 0
        
        for word_data in words_data:
            word = word_data['word']
            chinese_meaning = word_data['chinese_meaning']
            grade = word_data['grade']
            unit = word_data['unit']
            
            # 检查是否已存在相同的词汇
            existing_word = Word.query.filter_by(
                word=word, 
                grade=grade, 
                unit=unit
            ).first()
            
            if existing_word:
                # 更新现有词汇的中文含义
                if existing_word.chinese_meaning != chinese_meaning:
                    existing_word.chinese_meaning = chinese_meaning
                    updated_count += 1
                    print(f"更新: {word} ({grade}年级第{unit}单元) -> {chinese_meaning}")
            else:
                # 添加新词汇
                new_word = Word(
                    word=word,
                    chinese_meaning=chinese_meaning,
                    grade=grade,
                    unit=unit
                )
                db.session.add(new_word)
                imported_count += 1
                print(f"添加: {word} ({grade}年级第{unit}单元) -> {chinese_meaning}")
        
        db.session.commit()
        return imported_count, updated_count
        
    except Exception as e:
        print(f"导入文件 {json_file} 时出错: {e}")
        db.session.rollback()
        return 0, 0

def import_all_grade_words():
    """导入所有年级的词汇"""
    app = create_app()
    
    with app.app_context():
        print("🚀 开始导入人教版PEP小学英语词库")
        print("="*60)
        
        # 要导入的文件列表
        json_files = [
            'grade3_words_part1.json',
            'grade3_words_part2.json', 
            'grade4_words.json',
            'grade5_words.json',
            'grade6_words.json'
        ]
        
        total_imported = 0
        total_updated = 0
        
        for json_file in json_files:
            if os.path.exists(json_file):
                print(f"\n📚 导入 {json_file}...")
                imported, updated = import_words_from_json(json_file)
                total_imported += imported
                total_updated += updated
                print(f"✅ {json_file}: 新增 {imported} 个词汇, 更新 {updated} 个词汇")
            else:
                print(f"❌ 文件不存在: {json_file}")
        
        print(f"\n🎉 导入完成!")
        print(f"📊 总计: 新增 {total_imported} 个词汇, 更新 {total_updated} 个词汇")
        
        # 统计最终结果
        print(f"\n📈 词库统计:")
        total_words = Word.query.count()
        print(f"总词汇数: {total_words}")
        
        for grade in [3, 4, 5, 6]:
            count = Word.query.filter_by(grade=grade).count()
            print(f"{grade}年级: {count}个词汇")
            
            if count > 0:
                units = db.session.query(Word.unit).filter_by(grade=grade).distinct().all()
                unit_list = sorted([u[0] for u in units if u[0] is not None])
                print(f"  单元: {unit_list}")

def check_word_requirements():
    """检查词汇数量是否符合教材标准"""
    app = create_app()
    
    with app.app_context():
        print("\n🔍 检查词汇数量是否符合2024年新版人教版PEP教材标准")
        print("="*60)
        
        # 标准要求
        requirements = {
            3: 190,  # 三年级约190个词汇
            4: 210,  # 四年级约210个词汇  
            5: 230,  # 五年级约230个词汇
            6: 165   # 六年级约140-190个词汇（取中间值165）
        }
        
        for grade, required in requirements.items():
            actual = Word.query.filter_by(grade=grade).count()
            percentage = (actual / required) * 100
            
            status = "✅" if actual >= required else "⚠️" if percentage >= 80 else "❌"
            print(f"{status} {grade}年级: {actual}/{required} 个词汇 ({percentage:.1f}%)")
            
            if actual < required:
                missing = required - actual
                print(f"   还需要 {missing} 个词汇")

if __name__ == "__main__":
    # 导入词汇
    import_all_grade_words()
    
    # 检查是否符合标准
    check_word_requirements()