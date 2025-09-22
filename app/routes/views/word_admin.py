from flask import render_template, request, redirect, url_for, flash, jsonify
from app.routes.views import main
from app.models.word import Word
from app import db
import json
import os

@main.route('/admin/words')
def word_management():
    """词库管理页面"""
    # 统计当前词库数据
    stats = {}
    for grade in [3, 4, 5, 6]:
        count = Word.query.filter_by(grade=grade).count()
        stats[grade] = count
    
    total_words = Word.query.count()
    
    return render_template('admin/words.html', stats=stats, total_words=total_words)

@main.route('/admin/words/import', methods=['POST'])
def import_words():
    """导入词库数据"""
    try:
        # 要导入的文件列表（包含完整的六年级词库）
        files = [
            'grade3_words_part1.json',
            'grade3_words_part2.json', 
            'grade4_words.json',
            'grade5_words.json',
            'grade6_words.json',
            'grade6_words_complete.json',  # 完整的六年级词库
            'grade6_words_additional.json',  # 补充的六年级词库
            'grade6_words_extended.json'  # 扩展的六年级词库
        ]
        
        total_imported = 0
        results = []
        
        for file_name in files:
            file_path = os.path.join(os.getcwd(), file_name)
            
            if os.path.exists(file_path):
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
                
                results.append({
                    'file': file_name,
                    'imported': imported,
                    'total': len(words_data)
                })
                total_imported += imported
            else:
                results.append({
                    'file': file_name,
                    'error': '文件不存在'
                })
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'成功导入 {total_imported} 个词汇',
            'results': results
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@main.route('/admin/words/import_grade6', methods=['POST'])
def import_grade6_complete():
    """导入完整的六年级词库（解决用户反馈的问题）"""
    try:
        # 专门的六年级词库文件
        grade6_files = [
            'grade6_words_complete.json',  # 完整的新词库
            'grade6_words_additional.json',  # 补充词库
            'grade6_words_extended.json'  # 扩展词库
        ]
        
        total_imported = 0
        total_updated = 0
        results = []
        
        # 先统计原有的六年级词汇数量
        before_count = Word.query.filter_by(grade=6).count()
        
        for file_name in grade6_files:
            file_path = os.path.join(os.getcwd(), file_name)
            
            if os.path.exists(file_path):
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
                        continue
                    
                    # 检查是否已存在相同的词汇（同一年级的同一单词）
                    existing = Word.query.filter_by(
                        word=word, 
                        grade=grade
                    ).first()
                    
                    if existing:
                        # 更新现有词汇
                        if existing.chinese_meaning != chinese_meaning or existing.unit != unit:
                            existing.chinese_meaning = chinese_meaning
                            existing.unit = unit
                            updated += 1
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
                
                results.append({
                    'file': file_name,
                    'imported': imported,
                    'updated': updated,
                    'total': len(words_data)
                })
                total_imported += imported
                total_updated += updated
            else:
                results.append({
                    'file': file_name,
                    'error': '文件不存在'
                })
        
        db.session.commit()
        
        # 统计导入后的六年级词汇数量
        after_count = Word.query.filter_by(grade=6).count()
        
        return jsonify({
            'success': True,
            'message': f'六年级词库完善成功！新增 {total_imported} 个，更新 {total_updated} 个',
            'before_count': before_count,
            'after_count': after_count,
            'results': results,
            'source_info': {
                'description': '基于2024年最新人教版PEP小学英语六年级教材',
                'includes': ['交通方式', '地点方位', '计划安排', '爱好与活动', '职业与工作', '情感与态度'],
                'total_units': 6
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@main.route('/admin/words/check')
def check_words():
    """检查词库完整性"""
    try:
        # 标准要求
        requirements = {
            3: 190,  # 三年级约190个词汇
            4: 210,  # 四年级约210个词汇  
            5: 230,  # 五年级约230个词汇
            6: 165   # 六年级约140-190个词汇（取中间值165）
        }
        
        results = []
        for grade, required in requirements.items():
            actual = Word.query.filter_by(grade=grade).count()
            percentage = (actual / required) * 100 if required > 0 else 0
            
            results.append({
                'grade': grade,
                'actual': actual,
                'required': required,
                'percentage': round(percentage, 1),
                'status': 'complete' if actual >= required else 'incomplete'
            })
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500