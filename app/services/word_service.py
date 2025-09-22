from app.models.word import Word
from app import db
from sqlalchemy import func
import random
import logging

logger = logging.getLogger(__name__)

class WordService:
    """词库服务类"""
    
    @staticmethod
    def get_words_by_criteria(grade=None, unit=None, limit=None, offset=None):
        """根据条件获取单词列表"""
        # 尝试使用缓存
        try:
            from app.services.cache_service import WordCacheService
            if not offset and limit and limit <= 100:  # 只缓存简单查询
                cached_result = WordCacheService.get_words_by_criteria(grade, unit, limit, offset)
                if cached_result:
                    return [Word(**data) for data in cached_result if isinstance(data, dict)]
        except Exception as e:
            logger.warning(f"缓存查询失败，使用数据库查询: {str(e)}")
        
        # 数据库查询
        query = Word.query
        
        if grade:
            query = query.filter_by(grade=grade)
        if unit:
            query = query.filter_by(unit=unit)
        
        query = query.order_by(Word.grade, Word.unit, Word.id)
        
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    @staticmethod
    def get_word_by_id(word_id):
        """根据ID获取单词"""
        return Word.query.get(word_id)
    
    @staticmethod
    def search_words(keyword, grade=None):
        """搜索单词"""
        query = Word.query.filter(
            db.or_(
                Word.word.ilike(f'%{keyword}%'),
                Word.chinese_meaning.ilike(f'%{keyword}%')
            )
        )
        
        if grade:
            query = query.filter_by(grade=grade)
        
        return query.order_by(Word.grade, Word.unit).all()
    
    @staticmethod
    def get_random_words(grade=None, unit=None, count=10):
        """获取随机单词列表"""
        query = Word.query
        
        if grade:
            query = query.filter_by(grade=grade)
        if unit:
            query = query.filter_by(unit=unit)
        
        # 获取符合条件的所有单词ID
        word_ids = [w.id for w in query.with_entities(Word.id).all()]
        
        if len(word_ids) <= count:
            # 如果总数不足，返回所有符合条件的单词
            return query.all()
        
        # 随机选择指定数量的ID
        selected_ids = random.sample(word_ids, count)
        
        return Word.query.filter(Word.id.in_(selected_ids)).order_by(func.random()).all()
    
    @staticmethod
    def get_grade_units(grade):
        """获取指定年级的所有单元"""
        # 尝试使用缓存
        try:
            from app.services.cache_service import WordCacheService
            cached_result = WordCacheService.get_grade_units(grade)
            if cached_result is not None:
                return cached_result
        except Exception as e:
            logger.warning(f"缓存查询失败，使用数据库查询: {str(e)}")
        
        # 使用新的年级单元结构
        from app.utils.constants import get_grade_all_units
        return get_grade_all_units(grade)
    
    @staticmethod
    def get_all_grades():
        """获取所有年级"""
        # 尝试使用缓存
        try:
            from app.services.cache_service import WordCacheService
            cached_result = WordCacheService.get_all_grades()
            if cached_result is not None:
                return cached_result
        except Exception as e:
            logger.warning(f"缓存查询失败，使用数据库查询: {str(e)}")
        
        grades = db.session.query(Word.grade).distinct().order_by(Word.grade).all()
        return [grade[0] for grade in grades]
    
    @staticmethod
    def get_word_count(grade=None, unit=None):
        """获取单词总数"""
        query = Word.query
        
        if grade:
            query = query.filter_by(grade=grade)
        if unit:
            query = query.filter_by(unit=unit)
        
        return query.count()
    
    @staticmethod
    def create_word(word_data):
        """创建新单词"""
        # 验证年级和单元的组合
        from app.utils.error_handler import Validator
        grade = word_data.get('grade')
        unit = word_data.get('unit')
        
        if grade and unit:
            try:
                Validator.validate_grade_unit(grade, unit)
            except Exception as e:
                logger.warning(f"年级单元验证失败，但允许创建: {str(e)}")
        
        word = Word(
            word=word_data.get('word'),
            chinese_meaning=word_data.get('chinese_meaning'),
            phonetic=word_data.get('phonetic', ''),
            phonics_breakdown=word_data.get('phonics_breakdown', ''),
            memory_method=word_data.get('memory_method', ''),
            grade=grade,
            unit=unit,
            book_version=word_data.get('book_version', 'PEP'),
            audio_url=word_data.get('audio_url', '')
        )
        
        db.session.add(word)
        db.session.commit()
        
        # 清除相关缓存
        try:
            from app.services.cache_service import WordCacheService
            WordCacheService.clear_word_cache()
        except Exception as e:
            logger.warning(f"清除缓存失败: {str(e)}")
        
        return word
    
    @staticmethod
    def update_word(word_id, word_data):
        """更新单词信息"""
        word = Word.query.get(word_id)
        if not word:
            return None
        
        # 更新字段
        for key, value in word_data.items():
            if hasattr(word, key) and key != 'id':
                setattr(word, key, value)
        
        word.updated_at = db.func.now()
        db.session.commit()
        
        # 清除相关缓存
        try:
            from app.services.cache_service import WordCacheService
            WordCacheService.clear_word_cache()
        except Exception as e:
            logger.warning(f"清除缓存失败: {str(e)}")
        
        return word
    
    @staticmethod
    def delete_word(word_id):
        """删除单词"""
        word = Word.query.get(word_id)
        if not word:
            return False
        
        db.session.delete(word)
        db.session.commit()
        
        # 清除相关缓存
        try:
            from app.services.cache_service import WordCacheService
            WordCacheService.clear_word_cache()
        except Exception as e:
            logger.warning(f"清除缓存失败: {str(e)}")
        
        return True
    
    @staticmethod
    def bulk_create_words(words_data):
        """批量创建单词"""
        words = []
        for word_data in words_data:
            word = Word(
                word=word_data.get('word'),
                chinese_meaning=word_data.get('chinese_meaning'),
                phonetic=word_data.get('phonetic', ''),
                phonics_breakdown=word_data.get('phonics_breakdown', ''),
                memory_method=word_data.get('memory_method', ''),
                grade=word_data.get('grade'),
                unit=word_data.get('unit'),
                book_version=word_data.get('book_version', 'PEP'),
                audio_url=word_data.get('audio_url', '')
            )
            words.append(word)
        
        db.session.add_all(words)
        db.session.commit()
        
        # 清除相关缓存
        try:
            from app.services.cache_service import WordCacheService
            WordCacheService.clear_word_cache()
        except Exception as e:
            logger.warning(f"清除缓存失败: {str(e)}")
        
        return words
    
    @staticmethod
    def get_word_statistics():
        """获取词库统计信息"""
        total_words = Word.query.count()
        
        # 按年级统计
        grade_stats = db.session.query(
            Word.grade,
            func.count(Word.id).label('count')
        ).group_by(Word.grade).order_by(Word.grade).all()
        
        # 按年级和单元统计
        unit_stats = db.session.query(
            Word.grade,
            Word.unit,
            func.count(Word.id).label('count')
        ).group_by(Word.grade, Word.unit).order_by(Word.grade, Word.unit).all()
        
        return {
            'total_words': total_words,
            'grade_stats': [{'grade': g, 'count': c} for g, c in grade_stats],
            'unit_stats': [{'grade': g, 'unit': u, 'count': c} for g, u, c in unit_stats]
        }
    
    @staticmethod
    def generate_word_audio(word_id):
        """为单词生成音频文件"""
        from app.services.tts_service import TTSService
        
        word = Word.query.get(word_id)
        if not word:
            return None, "单词不存在"
        
        # 如果已有音频URL，先删除旧文件
        if word.audio_url:
            TTSService.delete_audio_file(word.audio_url)
        
        # 生成新的音频文件
        audio_url, error = TTSService.generate_word_audio(word)
        
        if error:
            return None, error
        
        # 更新数据库中的音频URL
        word.audio_url = audio_url
        word.updated_at = db.func.now()
        db.session.commit()
        
        logger.info(f"成功为单词 '{word.word}' 生成音频")
        return audio_url, None
    
    @staticmethod
    def batch_generate_audio(grade=None, unit=None, force_regenerate=False):
        """批量生成音频文件
        
        Args:
            grade (int): 年级筛选
            unit (int): 单元筛选
            force_regenerate (bool): 是否强制重新生成
        
        Returns:
            dict: 生成结果统计
        """
        from app.services.tts_service import TTSService
        
        query = Word.query
        
        if grade:
            query = query.filter_by(grade=grade)
        if unit:
            query = query.filter_by(unit=unit)
        
        # 如果不强制重新生成，只处理没有音频的单词
        if not force_regenerate:
            query = query.filter(db.or_(Word.audio_url.is_(None), Word.audio_url == ''))
        
        words = query.all()
        
        if not words:
            return {
                'success_count': 0,
                'error_count': 0,
                'errors': [],
                'message': '没有需要生成音频的单词'
            }
        
        results = TTSService.batch_generate_audio(words)
        
        # 批量更新数据库
        try:
            db.session.commit()
            logger.info(f"批量音频生成完成: 成功 {results['success_count']}, 失败 {results['error_count']}")
        except Exception as e:
            db.session.rollback()
            results['error_count'] += 1
            results['errors'].append(f"数据库更新失败: {str(e)}")
        
        return results
    
    @staticmethod
    def get_words_without_audio(grade=None, unit=None):
        """获取没有音频的单词列表"""
        query = Word.query.filter(db.or_(Word.audio_url.is_(None), Word.audio_url == ''))
        
        if grade:
            query = query.filter_by(grade=grade)
        if unit:
            query = query.filter_by(unit=unit)
        
        return query.order_by(Word.grade, Word.unit, Word.id).all()
    
    @staticmethod
    def validate_audio_files():
        """验证数据库中的音频文件是否存在
        
        Returns:
            dict: 验证结果
        """
        import os
        from flask import current_app
        
        words_with_audio = Word.query.filter(
            Word.audio_url.isnot(None),
            Word.audio_url != ''
        ).all()
        
        results = {
            'total_checked': len(words_with_audio),
            'valid_count': 0,
            'invalid_count': 0,
            'invalid_words': []
        }
        
        audio_folder = current_app.config.get('AUDIO_FOLDER', 'app/static/audio')
        
        for word in words_with_audio:
            filename = os.path.basename(word.audio_url)
            file_path = os.path.join(audio_folder, filename)
            
            if os.path.exists(file_path):
                results['valid_count'] += 1
            else:
                results['invalid_count'] += 1
                results['invalid_words'].append({
                    'id': word.id,
                    'word': word.word,
                    'audio_url': word.audio_url
                })
        
        return results