from flask import request, jsonify
from flask import request, jsonify
from app.routes.api import api
from app.services.test_service import TestService
from app.utils.param_helpers import safe_get_int_param, safe_int

@api.route('/test/generate', methods=['POST'])
def generate_test():
    """生成测验"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': '请提供测验参数'
            }), 400
        
        user_id = data.get('user_id')
        test_type = data.get('test_type')
        grade = safe_int(data.get('grade'))
        unit = safe_int(data.get('unit'))
        question_count = safe_int(data.get('question_count'), 10)
        
        if not user_id or not test_type:
            return jsonify({
                'success': False,
                'error': '用户ID和测验类型是必需的'
            }), 400
        
        test_data, error = TestService.generate_test(
            user_id, test_type, grade, unit, question_count
        )
        
        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 400
        
        return jsonify({
            'success': True,
            'data': test_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api.route('/test/answer', methods=['POST'])
def submit_answer():
    """提交测验答案"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': '请提供答案数据'
            }), 400
        
        test_id = data.get('test_id')
        question_id = data.get('question_id')
        answer = data.get('answer')
        
        if not all([test_id, question_id is not None, answer is not None]):
            return jsonify({
                'success': False,
                'error': '测验ID、题目ID和答案是必需的'
            }), 400
        
        result, error = TestService.submit_answer(test_id, question_id, answer)
        
        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 400
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api.route('/test/finish', methods=['POST'])
def finish_test():
    """完成测验"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': '请提供测验ID'
            }), 400
        
        test_id = data.get('test_id')
        
        if not test_id:
            return jsonify({
                'success': False,
                'error': '测验ID是必需的'
            }), 400
        
        result, error = TestService.finish_test(test_id)
        
        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 400
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api.route('/test/result/<test_id>', methods=['GET'])
def get_test_result(test_id):
    """获取测验结果"""
    try:
        result, error = TestService.get_test_result(test_id)
        
        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 400
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api.route('/test/history/<int:user_id>', methods=['GET'])
def get_test_history(user_id):
    """获取测验历史"""
    try:
        limit = safe_get_int_param(request.args, 'limit', 10)
        if limit is None or limit <= 0:
            limit = 10
        
        history, error = TestService.get_user_test_history(user_id, limit)
        
        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 400
        
        return jsonify({
            'success': True,
            'data': history,
            'count': len(history) if history else 0
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api.route('/test/statistics/<int:user_id>', methods=['GET'])
def get_test_statistics(user_id):
    """获取测验统计"""
    try:
        stats, error = TestService.get_test_statistics(user_id)
        
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

@api.route('/test/retry', methods=['POST'])
def retry_wrong_words():
    """重新测验错题"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': '请提供重测参数'
            }), 400
        
        user_id = data.get('user_id')
        original_test_id = data.get('original_test_id')
        
        if not user_id or not original_test_id:
            return jsonify({
                'success': False,
                'error': '用户ID和原测验ID是必需的'
            }), 400
        
        retry_test, error = TestService.retry_wrong_words(user_id, original_test_id)
        
        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 400
        
        return jsonify({
            'success': True,
            'data': retry_test
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500