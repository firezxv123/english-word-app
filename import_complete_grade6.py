#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
完整的六年级词库导入脚本
基于2024年最新人教版PEP六年级教材，包含完整的词汇内容
"""

import sys
import os
import json
sys.path.insert(0, os.path.abspath('.'))

from app import create_app, db
from app.models.word import Word

def import_complete_grade6_words():
    """导入完整的六年级词汇"""
    app = create_app()
    
    with app.app_context():
        print("🚀 开始导入完整的六年级词库")
        print("="*50)
        
        # 要导入的六年级词汇文件
        grade6_files = [
            'grade6_words_complete.json',  # 新的完整词库
            'grade6_words_additional.json',  # 之前的补充词库
            'grade6_words_extended.json'     # 之前的扩展词库
        ]
        
        total_imported = 0
        total_updated = 0
        
        for file_name in grade6_files:
            file_path = os.path.join(os.getcwd(), file_name)
            
            if not os.path.exists(file_path):
                print(f"⚠️  文件不存在: {file_name}")
                continue
                
            print(f"\n📁 处理文件: {file_name}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    words_data = json.load(f)
                
                imported = 0
                updated = 0
                
                for word_data in words_data:
                    word = word_data.get('word', '').strip()
                    chinese_meaning = word_data.get('chinese_meaning', '').strip()
                    grade = word_data.get('grade', 6)
                    unit = word_data.get('unit', 1)
                    
                    if not word or not chinese_meaning:
                        print(f"⚠️  跳过空词汇: {word_data}")
                        continue
                    
                    # 检查是否已存在相同的词汇
                    existing_word = Word.query.filter_by(
                        word=word, 
                        grade=grade
                    ).first()
                    
                    if existing_word:
                        # 更新现有词汇
                        if existing_word.chinese_meaning != chinese_meaning or existing_word.unit != unit:
                            existing_word.chinese_meaning = chinese_meaning
                            existing_word.unit = unit
                            updated += 1
                            print(f"✏️  更新: {word} -> {chinese_meaning} ({grade}年级第{unit}单元)")
                    else:
                        # 添加新词汇
                        new_word = Word(
                            word=word,
                            chinese_meaning=chinese_meaning,
                            grade=grade,
                            unit=unit
                        )
                        db.session.add(new_word)
                        imported += 1
                        print(f"➕ 新增: {word} -> {chinese_meaning} ({grade}年级第{unit}单元)")
                
                total_imported += imported
                total_updated += updated
                
                print(f"📊 {file_name}: 新增 {imported} 个，更新 {updated} 个")
                
            except Exception as e:
                print(f"❌ 处理文件 {file_name} 时出错: {str(e)}")
                continue
        
        # 提交所有更改
        try:
            db.session.commit()
            print(f"\n✅ 导入完成!")
            print(f"📈 总计: 新增 {total_imported} 个词汇，更新 {total_updated} 个词汇")
            
            # 统计六年级词汇总数
            grade6_total = Word.query.filter_by(grade=6).count()
            print(f"📚 六年级词汇总数: {grade6_total} 个")
            
            # 按单元统计
            print(f"\n📋 按单元分布:")
            for unit in range(1, 11):  # 六年级最多10个单元
                count = Word.query.filter_by(grade=6, unit=unit).count()
                if count > 0:
                    print(f"   第{unit}单元: {count} 个词汇")
                    
        except Exception as e:
            db.session.rollback()
            print(f"❌ 提交失败: {str(e)}")

def check_grade6_completeness():
    """检查六年级词库完整性"""
    app = create_app()
    
    with app.app_context():
        print("\n🔍 检查六年级词库完整性")
        print("="*40)
        
        total = Word.query.filter_by(grade=6).count()
        print(f"📊 六年级总词汇数: {total}")
        
        # 分析词汇分布
        units_distribution = {}
        for unit in range(1, 11):
            count = Word.query.filter_by(grade=6, unit=unit).count()
            if count > 0:
                units_distribution[unit] = count
        
        print(f"📋 单元分布: {units_distribution}")
        
        # 评估完整性
        if total >= 160:
            status = "✅ 优秀"
        elif total >= 120:
            status = "🟨 良好"
        elif total >= 80:
            status = "🟧 需要补充"
        else:
            status = "❌ 严重不足"
            
        print(f"📈 完整性评估: {status} ({total}/160-180个目标词汇)")
        
        # 显示一些样例词汇
        sample_words = Word.query.filter_by(grade=6).limit(10).all()
        print(f"\n📖 词汇样例:")
        for word in sample_words:
            print(f"   {word.word} -> {word.chinese_meaning} (第{word.unit}单元)")

def clean_duplicate_words():
    """清理重复词汇"""
    app = create_app()
    
    with app.app_context():
        print("\n🧹 清理重复词汇")
        print("="*30)
        
        # 查找重复的词汇（相同的word和grade）
        duplicates = db.session.query(Word.word, Word.grade)\
            .group_by(Word.word, Word.grade)\
            .having(db.func.count(Word.id) > 1)\
            .all()
        
        if not duplicates:
            print("✅ 没有发现重复词汇")
            return
            
        print(f"⚠️  发现 {len(duplicates)} 组重复词汇")
        
        cleaned_count = 0
        for word_text, grade in duplicates:
            # 获取所有重复的记录
            duplicate_records = Word.query.filter_by(word=word_text, grade=grade).all()
            
            if len(duplicate_records) <= 1:
                continue
                
            # 保留第一个，删除其余的
            keep_record = duplicate_records[0]
            for record in duplicate_records[1:]:
                print(f"🗑️  删除重复: {record.word} (ID: {record.id})")
                db.session.delete(record)
                cleaned_count += 1
        
        if cleaned_count > 0:
            db.session.commit()
            print(f"✅ 清理完成，删除了 {cleaned_count} 个重复词汇")
        else:
            print("✅ 没有重复词汇需要清理")

if __name__ == "__main__":
    print("🎯 六年级词库完整化程序")
    print("根据2024年最新人教版PEP教材标准")
    print()
    
    # 1. 清理重复词汇
    clean_duplicate_words()
    
    # 2. 导入完整词库
    import_complete_grade6_words()
    
    # 3. 检查完整性
    check_grade6_completeness()
    
    print("\n🎉 六年级词库更新完成!")
    print("词库来源: 2024年人教版PEP六年级上下册教材")
    print("包含: 基础词汇、重点句型、语法要点")