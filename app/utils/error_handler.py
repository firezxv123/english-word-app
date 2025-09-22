#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import traceback
from functools import wraps
from flask import jsonify, request, current_app
from datetime import datetime
import uuid

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class ErrorHandler:
    """统一错误处理类"""
    
    # 错误代码映射
    ERROR_CODES = {
        'VALIDATION_ERROR': 400,
        'NOT_FOUND': 404,
        'PERMISSION_DENIED': 403,
        'UNAUTHORIZED': 401,
        'SERVER_ERROR': 500,
        'BAD_REQUEST': 400,
        'CONFLICT': 409,
        'UNPROCESSABLE_ENTITY': 422
    }
    
    # 用户友好的错误消息
    USER_FRIENDLY_MESSAGES = {
        'VALIDATION_ERROR': '输入数据格式不正确',
        'NOT_FOUND': '请求的资源不存在',
        'PERMISSION_DENIED': '没有权限执行此操作',
        'UNAUTHORIZED': '需要登录才能访问',
        'SERVER_ERROR': '服务器内部错误，请稍后重试',
        'BAD_REQUEST': '请求格式不正确',
        'CONFLICT': '资源冲突，请检查数据',
        'UNPROCESSABLE_ENTITY': '无法处理的请求数据'
    }
    
    @staticmethod
    def handle_api_error(func):
        """API错误处理装饰器"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            request_id = str(uuid.uuid4())
            start_time = datetime.now()
            
            # 记录请求开始
            logger.info(f"API请求开始 - ID: {request_id}, 路径: {request.path}, 方法: {request.method}, IP: {request.remote_addr}")
            
            try:
                result = func(*args, **kwargs)
                
                # 记录成功响应
                duration = (datetime.now() - start_time).total_seconds()
                logger.info(f"API请求成功 - ID: {request_id}, 耗时: {duration:.3f}s")
                
                return result
                
            except ValidationError as e:
                return ErrorHandler._handle_validation_error(e, request_id)
            except NotFoundError as e:
                return ErrorHandler._handle_not_found_error(e, request_id)
            except PermissionError as e:
                return ErrorHandler._handle_permission_error(e, request_id)
            except ConflictError as e:
                return ErrorHandler._handle_conflict_error(e, request_id)
            except Exception as e:
                return ErrorHandler._handle_generic_error(e, request_id, start_time)
        
        return wrapper
    
    @staticmethod
    def _handle_validation_error(error, request_id):
        """处理验证错误"""
        logger.warning(f"验证错误 - ID: {request_id}, 错误: {str(error)}")
        
        return jsonify({
            'success': False,
            'error': str(error),
            'error_code': 'VALIDATION_ERROR',
            'request_id': request_id
        }), 400
    
    @staticmethod
    def _handle_not_found_error(error, request_id):
        """处理资源不存在错误"""
        logger.warning(f"资源不存在 - ID: {request_id}, 错误: {str(error)}")
        
        return jsonify({
            'success': False,
            'error': str(error),
            'error_code': 'NOT_FOUND',
            'request_id': request_id
        }), 404
    
    @staticmethod
    def _handle_permission_error(error, request_id):
        """处理权限错误"""
        logger.warning(f"权限错误 - ID: {request_id}, 错误: {str(error)}")
        
        return jsonify({
            'success': False,
            'error': '没有权限执行此操作',
            'error_code': 'PERMISSION_DENIED',
            'request_id': request_id
        }), 403
    
    @staticmethod
    def _handle_conflict_error(error, request_id):
        """处理冲突错误"""
        logger.warning(f"冲突错误 - ID: {request_id}, 错误: {str(error)}")
        
        return jsonify({
            'success': False,
            'error': str(error),
            'error_code': 'CONFLICT',
            'request_id': request_id
        }), 409
    
    @staticmethod
    def _handle_generic_error(error, request_id, start_time):
        """处理通用错误"""
        duration = (datetime.now() - start_time).total_seconds()
        error_details = traceback.format_exc()
        
        logger.error(f"未处理的错误 - ID: {request_id}, 耗时: {duration:.3f}s, 错误: {str(error)}, 堆栈: {error_details}")
        
        # 在开发环境显示详细错误信息
        if current_app.debug:
            return jsonify({
                'success': False,
                'error': str(error),
                'error_code': 'SERVER_ERROR',
                'request_id': request_id,
                'debug_info': error_details
            }), 500
        else:
            return jsonify({
                'success': False,
                'error': '服务器内部错误，请稍后重试',
                'error_code': 'SERVER_ERROR',
                'request_id': request_id
            }), 500
    
    @staticmethod
    def log_user_action(user_id, action, details=None):
        """记录用户操作日志"""
        log_data = {
            'user_id': user_id,
            'action': action,
            'timestamp': datetime.now().isoformat(),
            'ip': request.remote_addr if request else None,
            'user_agent': request.headers.get('User-Agent') if request else None,
            'details': details
        }
        
        logger.info(f"用户操作 - {log_data}")
    
    @staticmethod
    def log_system_event(event_type, message, level='info', **kwargs):
        """记录系统事件日志"""
        log_data = {
            'event_type': event_type,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            **kwargs
        }
        
        log_message = f"系统事件 - {log_data}"
        
        if level == 'debug':
            logger.debug(log_message)
        elif level == 'info':
            logger.info(log_message)
        elif level == 'warning':
            logger.warning(log_message)
        elif level == 'error':
            logger.error(log_message)
        elif level == 'critical':
            logger.critical(log_message)

# 自定义异常类
class ValidationError(Exception):
    """验证错误"""
    pass

class NotFoundError(Exception):
    """资源不存在错误"""
    pass

class ConflictError(Exception):
    """冲突错误"""
    pass

class BusinessLogicError(Exception):
    """业务逻辑错误"""
    pass

# 数据验证辅助函数
class Validator:
    """数据验证器"""
    
    @staticmethod
    def validate_required_fields(data, required_fields):
        """验证必需字段"""
        missing_fields = []
        for field in required_fields:
            if field not in data or data[field] is None or data[field] == '':
                missing_fields.append(field)
        
        if missing_fields:
            raise ValidationError(f"缺少必需字段: {', '.join(missing_fields)}")
    
    @staticmethod
    def validate_grade(grade):
        """验证年级"""
        if not isinstance(grade, int) or grade < 3 or grade > 6:
            raise ValidationError("年级必须在3-6之间")
    
    @staticmethod
    def validate_unit(unit):
        """验证单元"""
        if not isinstance(unit, int) or unit < 1:
            raise ValidationError("单元必须是正整数")
    
    @staticmethod
    def validate_grade_unit(grade, unit):
        """验证年级和单元的组合是否有效"""
        from app.utils.constants import get_grade_all_units
        
        Validator.validate_grade(grade)
        Validator.validate_unit(unit)
        
        valid_units = get_grade_all_units(grade)
        if unit not in valid_units:
            raise ValidationError(f"{grade}年级只有{len(valid_units)}个单元，单元{unit}不存在")
    
    @staticmethod
    def validate_mastery_level(level):
        """验证掌握程度"""
        if not isinstance(level, int) or level < 1 or level > 5:
            raise ValidationError("掌握程度必须在1-5之间")
    
    @staticmethod
    def validate_username(username):
        """验证用户名"""
        if not username or len(username.strip()) < 2:
            raise ValidationError("用户名不能为空且长度至少为2个字符")
        
        if len(username) > 20:
            raise ValidationError("用户名长度不能超过20个字符")
        
        # 检查字符是否合法（中文、英文、数字）
        import re
        if not re.match(r'^[\u4e00-\u9fa5a-zA-Z0-9_]+$', username):
            raise ValidationError("用户名只能包含中文、英文、数字和下划线")
    
    @staticmethod
    def validate_word_data(word_data):
        """验证单词数据"""
        Validator.validate_required_fields(word_data, ['word', 'chinese_meaning', 'grade', 'unit'])
        
        # 验证年级和单元
        Validator.validate_grade(word_data['grade'])
        Validator.validate_unit(word_data['unit'])
        
        # 验证单词格式
        word = word_data['word'].strip()
        if not word:
            raise ValidationError("单词不能为空")
        
        if len(word) > 50:
            raise ValidationError("单词长度不能超过50个字符")
        
        # 验证中文含义
        chinese_meaning = word_data['chinese_meaning'].strip()
        if not chinese_meaning:
            raise ValidationError("中文含义不能为空")
        
        if len(chinese_meaning) > 200:
            raise ValidationError("中文含义长度不能超过200个字符")