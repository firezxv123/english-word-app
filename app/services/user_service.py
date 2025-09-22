#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.models.user import User
from app import db
from app.utils.error_handler import ValidationError, NotFoundError, ConflictError, Validator, ErrorHandler
import logging

logger = logging.getLogger(__name__)

class UserService:
    """用户服务类"""
    
    @staticmethod
    def create_user(username, grade):
        """创建新用户"""
        # 验证输入
        Validator.validate_username(username)
        Validator.validate_grade(grade)
        
        # 检查用户名是否已存在
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            raise ConflictError('用户名已存在')
        
        # 创建用户
        user = User(username=username.strip(), grade=grade)
        db.session.add(user)
        db.session.commit()
        
        # 记录日志
        ErrorHandler.log_system_event('user_created', f'新用户创建: {username}, 年级: {grade}')
        
        return user
    
    @staticmethod
    def get_user_by_id(user_id):
        """根据ID获取用户"""
        if not user_id or not isinstance(user_id, int):
            raise ValidationError('无效的用户ID')
        
        return User.query.get(user_id)
    
    @staticmethod
    def get_user_by_username(username):
        """根据用户名获取用户"""
        if not username:
            raise ValidationError('用户名不能为空')
        
        return User.query.filter_by(username=username.strip()).first()
    
    @staticmethod
    def update_user(user_id, **kwargs):
        """更新用户信息"""
        user = UserService.get_user_by_id(user_id)
        if not user:
            raise NotFoundError('用户不存在')
        
        # 验证更新数据
        if 'username' in kwargs:
            new_username = kwargs['username']
            Validator.validate_username(new_username)
            
            # 检查新用户名是否已被其他用户使用
            existing_user = User.query.filter(
                User.username == new_username.strip(),
                User.id != user_id
            ).first()
            
            if existing_user:
                raise ConflictError('用户名已被使用')
            
            user.username = new_username.strip()
        
        if 'grade' in kwargs:
            Validator.validate_grade(kwargs['grade'])
            user.grade = kwargs['grade']
        
        if 'current_unit' in kwargs:
            Validator.validate_unit(kwargs['current_unit'])
            user.current_unit = kwargs['current_unit']
        
        db.session.commit()
        
        # 清除相关缓存
        try:
            from app.services.cache_service import UserCacheService
            UserCacheService.clear_user_cache(user_id)
        except Exception as e:
            logger.warning(f"清除缓存失败: {str(e)}")
        
        # 记录日志
        ErrorHandler.log_system_event('user_updated', f'用户更新: {user.username}', details=kwargs)
        
        return user
    
    @staticmethod
    def delete_user(user_id):
        """删除用户"""
        user = UserService.get_user_by_id(user_id)
        if not user:
            raise NotFoundError('用户不存在')
        
        username = user.username
        db.session.delete(user)
        db.session.commit()
        
        # 清除相关缓存
        try:
            from app.services.cache_service import UserCacheService
            UserCacheService.clear_user_cache(user_id)
        except Exception as e:
            logger.warning(f"清除缓存失败: {str(e)}")
        
        # 记录日志
        ErrorHandler.log_system_event('user_deleted', f'用户删除: {username}')
        
        return True
    
    @staticmethod
    def get_all_users():
        """获取所有用户"""
        # 尝试使用缓存
        try:
            from app.services.cache_service import UserCacheService
            cached_users = UserCacheService.get_all_users()
            if cached_users:
                return [User(**data) for data in cached_users if isinstance(data, dict)]
        except Exception as e:
            logger.warning(f"缓存查询失败，使用数据库查询: {str(e)}")
        
        return User.query.order_by(User.created_at.desc()).all()
    
    @staticmethod
    def get_users_by_grade(grade):
        """根据年级获取用户"""
        Validator.validate_grade(grade)
        return User.query.filter_by(grade=grade).order_by(User.username).all()
    
    @staticmethod
    def get_user_statistics():
        """获取用户统计信息"""
        from sqlalchemy import func
        
        total_users = User.query.count()
        
        # 按年级统计
        grade_stats = db.session.query(
            User.grade,
            func.count(User.id).label('count')
        ).group_by(User.grade).order_by(User.grade).all()
        
        return {
            'total_users': total_users,
            'grade_stats': [{'grade': g, 'count': c} for g, c in grade_stats]
        }
    
    @staticmethod
    def validate_user_data(data, update=False):
        """验证用户数据（用于批量导入等）"""
        required_fields = ['username', 'grade'] if not update else []
        
        # 检查必填字段
        if required_fields:
            Validator.validate_required_fields(data, required_fields)
        
        # 验证用户名
        if 'username' in data:
            Validator.validate_username(data['username'])
        
        # 验证年级
        if 'grade' in data:
            Validator.validate_grade(data['grade'])
        
        # 验证当前单元
        if 'current_unit' in data:
            Validator.validate_unit(data['current_unit'])
    
    @staticmethod
    def search_users(keyword):
        """搜索用户"""
        if not keyword:
            return []
        
        keyword = keyword.strip()
        return User.query.filter(
            User.username.ilike(f'%{keyword}%')
        ).order_by(User.username).all()
    
    @staticmethod
    def get_user_detailed_info(user_id):
        """获取用户详细信息"""
        user = UserService.get_user_by_id(user_id)
        if not user:
            raise NotFoundError('用户不存在')
        
        # 尝试使用缓存获取学习进度
        try:
            from app.services.cache_service import UserCacheService
            cached_progress = UserCacheService.get_user_progress(user_id)
            if cached_progress:
                study_progress = cached_progress
            else:
                study_progress = user.get_study_progress()
        except Exception as e:
            logger.warning(f"缓存查询失败，使用数据库查询: {str(e)}")
            study_progress = user.get_study_progress()
        
        # 获取最近测验记录
        recent_tests = user.get_recent_tests(10)
        
        # 获取测验统计
        from app.models.test_record import TestRecord
        test_stats = TestRecord.get_user_test_stats(user_id, days=30)
        
        return {
            'user': user.to_dict(),
            'study_progress': study_progress,
            'recent_tests': [test.to_dict() for test in recent_tests],
            'test_statistics': test_stats
        }
    
    @staticmethod
    def update_user_study_progress(user_id, unit=None):
        """更新用户学习进度"""
        user = UserService.get_user_by_id(user_id)
        if not user:
            raise NotFoundError('用户不存在')
        
        if unit is not None:
            Validator.validate_unit(unit)
            user.current_unit = unit
            db.session.commit()
            
            # 清除相关缓存
            try:
                from app.services.cache_service import UserCacheService
                UserCacheService.clear_user_cache(user_id)
            except Exception as e:
                logger.warning(f"清除缓存失败: {str(e)}")
            
            # 记录日志
            ErrorHandler.log_user_action(user_id, 'progress_update', {'unit': unit})
        
        return user
