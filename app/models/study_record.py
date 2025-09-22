from datetime import datetime
from app import db

class StudyRecord(db.Model):
    """学习记录模型"""
    __tablename__ = 'study_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    word_id = db.Column(db.Integer, db.ForeignKey('words.id'), nullable=False, index=True)
    studied_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    mastery_level = db.Column(db.Integer, nullable=False, default=1)  # 掌握程度 1-5
    
    # 复合唯一索引，确保一个用户对一个单词只有一条最新记录
    __table_args__ = (
        db.Index('idx_study_records_user_word', 'user_id', 'word_id'),
    )
    
    def __repr__(self):
        return f'<StudyRecord user:{self.user_id} word:{self.word_id} level:{self.mastery_level}>'
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'word_id': self.word_id,
            'studied_at': self.studied_at.isoformat() if self.studied_at and hasattr(self.studied_at, 'isoformat') else str(self.studied_at) if self.studied_at else None,
            'mastery_level': self.mastery_level,
            'word': self.word.to_dict() if self.word else None
        }
    
    @staticmethod
    def update_or_create(user_id, word_id, mastery_level):
        """更新或创建学习记录"""
        record = StudyRecord.query.filter_by(user_id=user_id, word_id=word_id).first()
        
        if record:
            # 更新现有记录
            record.mastery_level = mastery_level
            record.studied_at = datetime.utcnow()
        else:
            # 创建新记录
            record = StudyRecord(
                user_id=user_id,
                word_id=word_id,
                mastery_level=mastery_level
            )
            db.session.add(record)
        
        db.session.commit()
        return record
    
    @staticmethod
    def get_user_progress(user_id, grade=None, unit=None):
        """获取用户学习进度"""
        from app.models.word import Word
        
        query = StudyRecord.query.filter_by(user_id=user_id)
        
        if grade or unit:
            query = query.join(Word)
            if grade:
                query = query.filter(Word.grade == grade)
            if unit:
                query = query.filter(Word.unit == unit)
        
        records = query.all()
        
        if not records:
            return {
                'total_words': 0,
                'studied_words': 0,
                'mastered_words': 0,
                'average_mastery': 0,
                'progress_rate': 0
            }
        
        studied_words = len(records)
        mastered_words = len([r for r in records if r.mastery_level >= 4])
        average_mastery = sum(r.mastery_level for r in records) / studied_words
        
        # 获取总单词数
        word_query = Word.query
        if grade:
            word_query = word_query.filter_by(grade=grade)
        if unit:
            word_query = word_query.filter_by(unit=unit)
        
        total_words = word_query.count()
        progress_rate = (studied_words / total_words * 100) if total_words > 0 else 0
        
        return {
            'total_words': total_words,
            'studied_words': studied_words,
            'mastered_words': mastered_words,
            'average_mastery': round(average_mastery, 1),
            'progress_rate': round(progress_rate, 1),
            'mastery_rate': round((mastered_words / studied_words * 100) if studied_words > 0 else 0, 1)
        }