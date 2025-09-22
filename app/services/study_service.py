from app.models.user import User
from app.models.study_record import StudyRecord
from app.services.word_service import WordService
from app import db
from datetime import datetime, timedelta
import random

class StudyService:
    """学习服务类"""
    
    @staticmethod
    def start_study_session(user_id, grade, unit=None):
        """开始学习会话"""
        user = User.query.get(user_id)
        if not user:
            return None, "用户不存在"
        
        # 获取学习单词列表
        words = WordService.get_words_by_criteria(grade=grade, unit=unit)
        if not words:
            return None, "没有找到符合条件的单词"
        
        # 获取用户的学习记录，优先显示未掌握的单词
        studied_word_ids = [r.word_id for r in 
                           StudyRecord.query.filter_by(user_id=user_id).all()]
        
        # 分为已学习和未学习的单词
        unstudied_words = [w for w in words if w.id not in studied_word_ids]
        studied_words = [w for w in words if w.id in studied_word_ids]
        
        # 获取未掌握的单词（掌握程度<4）
        unmastered_records = StudyRecord.query.filter(
            StudyRecord.user_id == user_id,
            StudyRecord.word_id.in_([w.id for w in studied_words]),
            StudyRecord.mastery_level < 4
        ).all()
        
        unmastered_word_ids = [r.word_id for r in unmastered_records]
        unmastered_words = [w for w in studied_words if w.id in unmastered_word_ids]
        
        # 学习顺序：未掌握的单词 -> 未学习的单词 -> 已掌握的单词
        study_order = unmastered_words + unstudied_words + \
                     [w for w in studied_words if w.id not in unmastered_word_ids]
        
        return {
            'session_id': f"study_{user_id}_{datetime.now().timestamp()}",
            'user': user.to_dict(),
            'words': [w.to_dict() for w in study_order],
            'total_count': len(study_order),
            'unstudied_count': len(unstudied_words),
            'unmastered_count': len(unmastered_words)
        }, None
    
    @staticmethod
    def record_study_progress(user_id, word_id, mastery_level):
        """记录学习进度"""
        if not (1 <= mastery_level <= 5):
            return None, "掌握程度必须在1-5之间"
        
        user = User.query.get(user_id)
        if not user:
            return None, "用户不存在"
        
        word = WordService.get_word_by_id(word_id)
        if not word:
            return None, "单词不存在"
        
        # 更新或创建学习记录
        record = StudyRecord.update_or_create(user_id, word_id, mastery_level)
        
        return record.to_dict(), None
    
    @staticmethod
    def get_study_progress(user_id, grade=None, unit=None):
        """获取学习进度"""
        user = User.query.get(user_id)
        if not user:
            return None, "用户不存在"
        
        progress_data = StudyRecord.get_user_progress(user_id, grade, unit)
        
        # 获取最近学习的单词
        recent_records = StudyRecord.query.filter_by(user_id=user_id)\
            .order_by(StudyRecord.studied_at.desc())\
            .limit(10).all()
        
        return {
            'user': user.to_dict(),
            'progress': progress_data,
            'recent_words': [r.to_dict() for r in recent_records]
        }, None
    
    @staticmethod
    def get_recommended_words(user_id, count=10):
        """获取推荐复习的单词"""
        user = User.query.get(user_id)
        if not user:
            return [], "用户不存在"
        
        # 获取用户未掌握的单词（掌握程度<4）
        unmastered_records = StudyRecord.query.filter(
            StudyRecord.user_id == user_id,
            StudyRecord.mastery_level < 4
        ).order_by(StudyRecord.studied_at.asc()).limit(count).all()
        
        recommended_words = [r.word for r in unmastered_records if r.word]
        
        # 如果未掌握的单词不够，补充该年级的新单词
        if len(recommended_words) < count:
            studied_word_ids = [r.word_id for r in 
                               StudyRecord.query.filter_by(user_id=user_id).all()]
            
            new_words = WordService.get_words_by_criteria(
                grade=user.grade,
                limit=count - len(recommended_words)
            )
            
            for word in new_words:
                if word.id not in studied_word_ids:
                    recommended_words.append(word)
                    if len(recommended_words) >= count:
                        break
        
        return [w.to_dict() for w in recommended_words], None
    
    @staticmethod
    def get_study_statistics(user_id, days=7):
        """获取学习统计"""
        user = User.query.get(user_id)
        if not user:
            return None, "用户不存在"
        
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # 获取时间段内的学习记录
        records = StudyRecord.query.filter(
            StudyRecord.user_id == user_id,
            StudyRecord.studied_at >= start_date
        ).all()
        
        # 按日期统计
        daily_stats = {}
        for record in records:
            date_key = record.studied_at.strftime('%Y-%m-%d')
            if date_key not in daily_stats:
                daily_stats[date_key] = {
                    'date': date_key,
                    'studied_count': 0,
                    'mastered_count': 0
                }
            
            daily_stats[date_key]['studied_count'] += 1
            if record.mastery_level >= 4:
                daily_stats[date_key]['mastered_count'] += 1
        
        # 总体统计
        total_progress = StudyRecord.get_user_progress(user_id)
        
        return {
            'user': user.to_dict(),
            'daily_stats': list(daily_stats.values()),
            'total_progress': total_progress,
            'period': {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'days': days
            }
        }, None
    
    @staticmethod
    def get_mastery_distribution(user_id):
        """获取掌握程度分布"""
        user = User.query.get(user_id)
        if not user:
            return None, "用户不存在"
        
        # 统计各掌握程度的单词数量
        mastery_stats = db.session.query(
            StudyRecord.mastery_level,
            db.func.count(StudyRecord.id).label('count')
        ).filter_by(user_id=user_id).group_by(StudyRecord.mastery_level).all()
        
        mastery_distribution = {}
        for level, count in mastery_stats:
            mastery_distribution[level] = count
        
        # 补充缺失的等级
        for level in range(1, 6):
            if level not in mastery_distribution:
                mastery_distribution[level] = 0
        
        return {
            'user': user.to_dict(),
            'mastery_distribution': mastery_distribution,
            'mastery_labels': {
                1: '初次接触',
                2: '有印象',
                3: '基本认识',
                4: '较熟练',
                5: '完全掌握'
            }
        }, None