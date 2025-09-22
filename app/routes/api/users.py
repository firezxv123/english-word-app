from flask import request, jsonify
from app.routes.api import api
from app.models.user import User
from app.services.user_service import UserService
from app.utils.error_handler import ErrorHandler, ValidationError, NotFoundError
from app import db

@api.route('/users', methods=['GET'])
@ErrorHandler.handle_api_error
def get_users():
    """获取用户列表"""
    users = UserService.get_all_users()
    
    return jsonify({
        'success': True,
        'data': [user.to_dict() for user in users],
        'count': len(users)
    })

@api.route('/users', methods=['POST'])
@ErrorHandler.handle_api_error
def create_user():
    """创建用户"""
    data = request.get_json()
    
    if not data:
        raise ValidationError('请提供用户数据')
    
    username = data.get('username')
    grade = data.get('grade')
    
    if not username or not grade:
        raise ValidationError('用户名和年级是必需的')
    
    # 创建用户
    user = UserService.create_user(username, grade)
    
    return jsonify({
        'success': True,
        'data': user.to_dict()
    }), 201

@api.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """获取用户信息"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': '用户不存在'
            }), 404
        
        # 获取用户学习进度
        progress = user.get_study_progress()
        
        # 获取最近测验记录
        recent_tests = user.get_recent_tests(5)
        
        user_data = user.to_dict()
        user_data['study_progress'] = progress
        user_data['recent_tests'] = [test.to_dict() for test in recent_tests]
        
        return jsonify({
            'success': True,
            'data': user_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """更新用户信息"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': '用户不存在'
            }), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': '请提供更新数据'
            }), 400
        
        # 更新用户信息
        if 'username' in data:
            # 检查新用户名是否已被其他用户使用
            existing_user = User.query.filter(
                User.username == data['username'],
                User.id != user_id
            ).first()
            
            if existing_user:
                return jsonify({
                    'success': False,
                    'error': '用户名已被使用'
                }), 400
            
            user.username = data['username']
        
        if 'grade' in data:
            grade = data['grade']
            if grade < 3 or grade > 6:
                return jsonify({
                    'success': False,
                    'error': '年级必须在3-6之间'
                }), 400
            user.grade = grade
        
        if 'current_unit' in data:
            current_unit = data['current_unit']
            if current_unit < 1:
                return jsonify({
                    'success': False,
                    'error': '当前单元必须是正整数'
                }), 400
            user.current_unit = current_unit
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': user.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """删除用户"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': '用户不存在'
            }), 404
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '用户删除成功'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api.route('/users/<int:user_id>/dashboard', methods=['GET'])
def get_user_dashboard(user_id):
    """获取用户仪表板数据"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': '用户不存在'
            }), 404
        
        # 获取学习进度
        study_progress = user.get_study_progress()
        
        # 获取最近测验记录
        recent_tests = user.get_recent_tests(10)
        
        # 获取测验统计
        from app.models.test_record import TestRecord
        test_stats = TestRecord.get_user_test_stats(user_id, days=30)
        
        dashboard_data = {
            'user': user.to_dict(),
            'study_progress': study_progress,
            'recent_tests': [test.to_dict() for test in recent_tests],
            'test_statistics': test_stats
        }
        
        return jsonify({
            'success': True,
            'data': dashboard_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500