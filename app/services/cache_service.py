#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import threading
import json
import hashlib
from typing import Any, Optional, Dict
from functools import wraps
import logging

logger = logging.getLogger(__name__)

class MemoryCache:
    """简单的内存缓存实现"""
    
    def __init__(self, default_ttl=3600):
        self.cache: Dict[str, Dict] = {}
        self.default_ttl = default_ttl
        self.lock = threading.RLock()
        
        # 启动清理线程
        self._start_cleanup_thread()
    
    def _start_cleanup_thread(self):
        """启动过期缓存清理线程"""
        def cleanup():
            while True:
                try:
                    time.sleep(300)  # 每5分钟清理一次
                    self._cleanup_expired()
                except Exception as e:
                    logger.error(f"缓存清理失败: {str(e)}")
        
        thread = threading.Thread(target=cleanup, daemon=True)
        thread.start()
    
    def _cleanup_expired(self):
        """清理过期的缓存项"""
        current_time = time.time()
        with self.lock:
            expired_keys = []
            for key, data in self.cache.items():
                if data['expires_at'] < current_time:
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self.cache[key]
            
            if expired_keys:
                logger.info(f"清理了 {len(expired_keys)} 个过期缓存项")
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        with self.lock:
            if key not in self.cache:
                return None
            
            data = self.cache[key]
            if data['expires_at'] < time.time():
                del self.cache[key]
                return None
            
            data['access_count'] += 1
            data['last_accessed'] = time.time()
            return data['value']
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """设置缓存值"""
        if ttl is None:
            ttl = self.default_ttl
        
        with self.lock:
            self.cache[key] = {
                'value': value,
                'expires_at': time.time() + ttl,
                'created_at': time.time(),
                'last_accessed': time.time(),
                'access_count': 0,
                'ttl': ttl
            }
            return True
    
    def delete(self, key: str) -> bool:
        """删除缓存值"""
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                return True
            return False
    
    def clear(self) -> bool:
        """清空所有缓存"""
        with self.lock:
            self.cache.clear()
            return True
    
    def keys(self) -> list:
        """获取所有缓存键"""
        with self.lock:
            return list(self.cache.keys())
    
    def stats(self) -> dict:
        """获取缓存统计信息"""
        with self.lock:
            total_items = len(self.cache)
            total_access = sum(data['access_count'] for data in self.cache.values())
            
            return {
                'total_items': total_items,
                'total_access': total_access,
                'hit_rate': 0.0,  # 需要跟踪命中率
                'memory_usage': self._estimate_memory_usage()
            }
    
    def _estimate_memory_usage(self) -> int:
        """估算内存使用量（字节）"""
        try:
            # 粗略估算
            total_size = 0
            for key, data in self.cache.items():
                # 键的大小
                total_size += len(str(key).encode('utf-8'))
                # 值的大小（尝试序列化）
                try:
                    total_size += len(json.dumps(data['value'], default=str).encode('utf-8'))
                except:
                    total_size += 1024  # 如果无法序列化，估算1KB
                # 元数据大小
                total_size += 200  # 估算每个缓存项的元数据大小
            
            return total_size
        except Exception:
            return 0

class CacheService:
    """缓存服务"""
    
    # 全局缓存实例
    _instance = None
    _cache = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CacheService, cls).__new__(cls)
            cls._cache = MemoryCache()
        return cls._instance
    
    @classmethod
    def get_cache(cls) -> MemoryCache:
        """获取缓存实例"""
        if cls._cache is None:
            cls._cache = MemoryCache()
        return cls._cache
    
    @staticmethod
    def cache_key(*args, **kwargs) -> str:
        """生成缓存键"""
        # 将参数转换为字符串并生成哈希
        key_data = str(args) + str(sorted(kwargs.items()))
        return hashlib.md5(key_data.encode('utf-8')).hexdigest()
    
    @staticmethod
    def cached(ttl=3600, key_prefix=''):
        """缓存装饰器"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                cache = CacheService.get_cache()
                
                # 生成缓存键
                cache_key = f"{key_prefix}:{func.__name__}:{CacheService.cache_key(*args, **kwargs)}"
                
                # 尝试从缓存获取
                cached_result = cache.get(cache_key)
                if cached_result is not None:
                    logger.debug(f"缓存命中: {cache_key}")
                    return cached_result
                
                # 执行函数
                result = func(*args, **kwargs)
                
                # 存储到缓存
                cache.set(cache_key, result, ttl)
                logger.debug(f"缓存存储: {cache_key}")
                
                return result
            
            # 添加清除缓存的方法
            def clear_cache(*args, **kwargs):
                cache = CacheService.get_cache()
                cache_key = f"{key_prefix}:{func.__name__}:{CacheService.cache_key(*args, **kwargs)}"
                return cache.delete(cache_key)
            
            wrapper.clear_cache = clear_cache
            return wrapper
        
        return decorator

# 全局缓存实例
cache_service = CacheService()

# 词库相关缓存
class WordCacheService:
    """词库缓存服务"""
    
    @staticmethod
    @CacheService.cached(ttl=1800, key_prefix='words')  # 30分钟
    def get_words_by_criteria(grade=None, unit=None, limit=None, offset=None):
        """缓存单词查询"""
        from app.services.word_service import WordService
        return [word.to_dict() for word in WordService.get_words_by_criteria(grade, unit, limit, offset)]
    
    @staticmethod
    @CacheService.cached(ttl=3600, key_prefix='words')  # 1小时
    def get_word_statistics():
        """缓存词库统计"""
        from app.services.word_service import WordService
        return WordService.get_word_statistics()
    
    @staticmethod
    @CacheService.cached(ttl=3600, key_prefix='words')  # 1小时
    def get_all_grades():
        """缓存年级列表"""
        from app.services.word_service import WordService
        return WordService.get_all_grades()
    
    @staticmethod
    @CacheService.cached(ttl=3600, key_prefix='words')  # 1小时
    def get_grade_units(grade):
        """缓存年级单元"""
        from app.services.word_service import WordService
        return WordService.get_grade_units(grade)
    
    @staticmethod
    def clear_word_cache():
        """清除所有单词相关缓存"""
        cache = CacheService.get_cache()
        keys_to_delete = [key for key in cache.keys() if key.startswith('words:')]
        
        for key in keys_to_delete:
            cache.delete(key)
        
        logger.info(f"清除了 {len(keys_to_delete)} 个单词缓存项")

# 用户相关缓存
class UserCacheService:
    """用户缓存服务"""
    
    @staticmethod
    def get_user_progress(user_id):
        """缓存用户学习进度"""
        from app.models.user import User
        user = User.query.get(user_id)
        if user:
            return user.get_study_progress()
        return None
    
    @staticmethod
    def get_all_users():
        """缓存用户列表"""
        from app.models.user import User
        return [user.to_dict() for user in User.query.order_by(User.created_at.desc()).all()]
    
    @staticmethod
    def clear_user_cache(user_id=None):
        """清除用户缓存"""
        cache = CacheService.get_cache()
        
        if user_id:
            # 清除特定用户的缓存
            keys_to_delete = [key for key in cache.keys() 
                            if key.startswith('users:') and str(user_id) in key]
        else:
            # 清除所有用户缓存
            keys_to_delete = [key for key in cache.keys() if key.startswith('users:')]
        
        for key in keys_to_delete:
            cache.delete(key)
        
        logger.info(f"清除了 {len(keys_to_delete)} 个用户缓存项")

# 音频缓存服务
class AudioCacheService:
    """音频缓存服务"""
    
    @staticmethod
    @CacheService.cached(ttl=86400, key_prefix='audio')  # 24小时
    def get_word_audio_info(word_id):
        """缓存单词音频信息"""
        from app.services.tts_service import TTSService
        from app.services.word_service import WordService
        
        word = WordService.get_word_by_id(word_id)
        if word and word.audio_url:
            return TTSService.get_audio_info(word.audio_url)
        return None
    
    @staticmethod
    def clear_audio_cache():
        """清除音频缓存"""
        cache = CacheService.get_cache()
        keys_to_delete = [key for key in cache.keys() if key.startswith('audio:')]
        
        for key in keys_to_delete:
            cache.delete(key)
        
        logger.info(f"清除了 {len(keys_to_delete)} 个音频缓存项")