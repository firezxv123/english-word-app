#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request
from app.utils.error_handler import ErrorHandler
from app import db
from app.models.word import Word
import logging

logger = logging.getLogger(__name__)

from app.routes.api import api

@api.route('/maintenance/validate-units', methods=['GET'])
@ErrorHandler.handle_api_error
def validate_units():
    """验证单元数据"""
    # 统计各年级单元分布
    stats = {}
    
    for grade in [3, 4, 5, 6]:
        from sqlalchemy import func
        unit_stats = db.session.query(
            Word.unit,
            func.count(Word.id).label('count')
        ).filter_by(grade=grade).group_by(Word.unit).order_by(Word.unit).all()
        
        stats[grade] = [
            {'unit': unit, 'count': count} 
            for unit, count in unit_stats
        ]
    
    return jsonify({
        'success': True,
        'data': stats
    })

@api.route('/maintenance/fix-units', methods=['POST'])
@ErrorHandler.handle_api_error
def fix_units():
    """修复单元数据"""
    try:
        # 修复单元号大于12的单词
        words_to_fix = Word.query.filter(Word.unit > 12).all()
        fixed_count = 0
        
        for word in words_to_fix:
            logger.info(f"修复单词: {word.word} (年级:{word.grade}, 单元:{word.unit} -> 12)")
            word.unit = 12
            fixed_count += 1
        
        # 修复六年级单元号大于10的单词
        grade6_words = Word.query.filter(Word.grade == 6, Word.unit > 10).all()
        
        for word in grade6_words:
            logger.info(f"修复六年级单词: {word.word} (单元:{word.unit} -> 10)")
            word.unit = 10
            fixed_count += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'成功修复了{fixed_count}个单词的单元数据'
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"修复失败: {str(e)}")
        raise Exception(f"修复失败: {str(e)}")

@api.route('/maintenance/validate-params', methods=['POST'])
@ErrorHandler.handle_api_error
def validate_params():
    """验证API参数处理"""
    data = request.get_json() or {}
    
    # 测试空字符串转int的问题
    test_values = ['', '0', '3', 'abc', None]
    results = {}
    
    for val in test_values:
        try:
            if val == '':
                # 处理空字符串
                result = None
            elif val is None:
                result = None
            else:
                result = int(val)
            results[str(val)] = {'success': True, 'value': result}
        except ValueError as e:
            results[str(val)] = {'success': False, 'error': str(e)}
    
    return jsonify({
        'success': True,
        'data': results
    })

@api.route('/maintenance/check-system', methods=['GET'])
@ErrorHandler.handle_api_error
def check_system():
    """系统检查"""
    try:
        # 检查数据库连接
        db.session.execute('SELECT 1')
        
        # 检查词库状态
        word_count = Word.query.count()
        
        # 检查用户数量
        from app.models.user import User
        user_count = User.query.count()
        
        return jsonify({
            'success': True,
            'data': {
                'database': 'connected',
                'word_count': word_count,
                'user_count': user_count,
                'status': 'healthy'
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'系统检查失败: {str(e)}'
        }), 500

@api.route('/maintenance/cache-clear', methods=['POST'])
@ErrorHandler.handle_api_error
def clear_system_cache():
    """清除系统缓存"""
    try:
        from app.services.cache_service import CacheService
        cache = CacheService.get_cache()
        cache.clear()
        
        return jsonify({
            'success': True,
            'message': '系统缓存已清除'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'清除缓存失败: {str(e)}'
        }), 500