from flask import request, jsonify
from app.routes.api import api
from app.services.study_service import StudyService
from app.utils.param_helpers import safe_get_int_param

@api.route('/study/start', methods=['POST'])
def start_study():
    """开始学习会话"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': '请提供学习参数'
            }), 400
        
        user_id = data.get('user_id')
        grade = data.get('grade')
        unit = data.get('unit')
        
        if not user_id or not grade:
            return jsonify({
                'success': False,
                'error': '用户ID和年级是必需的'
            }), 400
        
        session_data, error = StudyService.start_study_session(user_id, grade, unit)
        
        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 400
        
        return jsonify({
            'success': True,
            'data': session_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api.route('/study/progress', methods=['POST'])
def record_progress():
    """记录学习进度"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': '请提供学习进度数据'
            }), 400
        
        user_id = data.get('user_id')
        word_id = data.get('word_id')
        mastery_level = data.get('mastery_level')
        
        if not all([user_id, word_id, mastery_level]):
            return jsonify({
                'success': False,
                'error': '用户ID、单词ID和掌握程度是必需的'
            }), 400
        
        record, error = StudyService.record_study_progress(user_id, word_id, mastery_level)
        
        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 400
        
        return jsonify({
            'success': True,
            'data': record
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api.route('/study/progress/<int:user_id>', methods=['GET'])
def get_study_progress(user_id):
    """获取学习进度"""
    try:
        grade = safe_get_int_param(request.args, 'grade')
        unit = safe_get_int_param(request.args, 'unit')
        
        progress, error = StudyService.get_study_progress(user_id, grade, unit)
        
        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 400
        
        return jsonify({
            'success': True,
            'data': progress
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api.route('/study/recommended/<int:user_id>', methods=['GET'])
def get_recommended_words(user_id):
    """获取推荐学习的单词"""
    try:
        count = safe_get_int_param(request.args, 'count', 10)
        
        words, error = StudyService.get_recommended_words(user_id, count)
        
        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 400
        
        return jsonify({
            'success': True,
            'data': words,
            'count': len(words)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api.route('/study/statistics/<int:user_id>', methods=['GET'])
def get_study_statistics(user_id):
    """获取学习统计"""
    try:
        days = safe_get_int_param(request.args, 'days', 7)
        
        stats, error = StudyService.get_study_statistics(user_id, days)
        
        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 400
        
        return jsonify({
            'success': True,
            'data': stats
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api.route('/study/mastery/<int:user_id>', methods=['GET'])
def get_mastery_distribution(user_id):
    """获取掌握程度分布"""
    try:
        distribution, error = StudyService.get_mastery_distribution(user_id)
        
        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 400
        
        return jsonify({
            'success': True,
            'data': distribution
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500