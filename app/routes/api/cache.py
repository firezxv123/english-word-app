#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request
from app.utils.error_handler import ErrorHandler
from app.services.cache_service import CacheService, WordCacheService, UserCacheService, AudioCacheService
import logging

logger = logging.getLogger(__name__)

from app.routes.api import api

@api.route('/cache/stats', methods=['GET'])
@ErrorHandler.handle_api_error
def get_cache_stats():
    """获取缓存统计信息"""
    cache = CacheService.get_cache()
    stats = cache.stats()
    
    return jsonify({
        'success': True,
        'data': {
            'cache_stats': stats,
            'keys': cache.keys()
        }
    })

@api.route('/cache/clear', methods=['POST'])
@ErrorHandler.handle_api_error
def clear_cache():
    """清除缓存"""
    data = request.get_json() or {}
    cache_type = data.get('type', 'all')
    
    if cache_type == 'all':
        # 清除所有缓存
        cache = CacheService.get_cache()
        cache.clear()
        logger.info("清除了所有缓存")
        message = "所有缓存已清除"
        
    elif cache_type == 'words':
        # 清除单词缓存
        WordCacheService.clear_word_cache()
        message = "单词缓存已清除"
        
    elif cache_type == 'users':
        # 清除用户缓存
        user_id = data.get('user_id')
        UserCacheService.clear_user_cache(user_id)
        message = f"用户缓存已清除" + (f" (用户ID: {user_id})" if user_id else "")
        
    elif cache_type == 'audio':
        # 清除音频缓存
        AudioCacheService.clear_audio_cache()
        message = "音频缓存已清除"
        
    else:
        return jsonify({
            'success': False,
            'error': '无效的缓存类型'
        }), 400
    
    return jsonify({
        'success': True,
        'message': message
    })

@api.route('/cache/key/<cache_key>', methods=['DELETE'])
@ErrorHandler.handle_api_error
def delete_cache_key(cache_key):
    """删除指定缓存键"""
    cache = CacheService.get_cache()
    success = cache.delete(cache_key)
    
    if success:
        return jsonify({
            'success': True,
            'message': f'缓存键 {cache_key} 已删除'
        })
    else:
        return jsonify({
            'success': False,
            'error': '缓存键不存在'
        }), 404

@api.route('/cache/key/<cache_key>', methods=['GET'])
@ErrorHandler.handle_api_error
def get_cache_value(cache_key):
    """获取指定缓存值"""
    cache = CacheService.get_cache()
    value = cache.get(cache_key)
    
    if value is not None:
        return jsonify({
            'success': True,
            'data': {
                'key': cache_key,
                'value': value
            }
        })
    else:
        return jsonify({
            'success': False,
            'error': '缓存键不存在或已过期'
        }), 404

@api.route('/cache/warmup', methods=['POST'])
@ErrorHandler.handle_api_error
def warmup_cache():
    """预热缓存"""
    data = request.get_json() or {}
    cache_types = data.get('types', ['words', 'users'])
    
    warmed_up = []
    
    try:
        if 'words' in cache_types:
            # 预热词库缓存
            from app.services.cache_service import WordCacheService
            
            # 预热年级列表
            WordCacheService.get_all_grades()
            warmed_up.append('words_grades')
            
            # 预热各年级的单元
            for grade in range(3, 7):
                WordCacheService.get_grade_units(grade)
                warmed_up.append(f'words_grade_{grade}_units')
            
            # 预热词库统计
            WordCacheService.get_word_statistics()
            warmed_up.append('words_statistics')
        
        if 'users' in cache_types:
            # 预热用户缓存
            from app.services.cache_service import UserCacheService
            
            # 预热用户列表
            UserCacheService.get_all_users()
            warmed_up.append('users_list')
        
        return jsonify({
            'success': True,
            'message': '缓存预热完成',
            'data': {
                'warmed_up': warmed_up,
                'count': len(warmed_up)
            }
        })
        
    except Exception as e:
        logger.error(f"缓存预热失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'缓存预热失败: {str(e)}'
        }), 500

@api.route('/cache/health', methods=['GET'])
@ErrorHandler.handle_api_error
def cache_health_check():
    """缓存健康检查"""
    try:
        cache = CacheService.get_cache()
        
        # 测试缓存读写
        test_key = 'health_check_test'
        test_value = 'test_data'
        
        # 写入测试
        cache.set(test_key, test_value, 60)
        
        # 读取测试
        retrieved_value = cache.get(test_key)
        
        # 清理测试数据
        cache.delete(test_key)
        
        if retrieved_value == test_value:
            stats = cache.stats()
            return jsonify({
                'success': True,
                'message': '缓存服务正常',
                'data': {
                    'status': 'healthy',
                    'stats': stats
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': '缓存读写测试失败'
            }), 500
            
    except Exception as e:
        logger.error(f"缓存健康检查失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'缓存健康检查失败: {str(e)}'
        }), 500