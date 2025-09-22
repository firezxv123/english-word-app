from datetime import datetime
from app import db

class Word(db.Model):
    """单词模型"""
    __tablename__ = 'words'
    
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False, index=True)
    chinese_meaning = db.Column(db.Text, nullable=False)
    phonetic = db.Column(db.String(200))
    phonics_breakdown = db.Column(db.Text)  # 自然拼读拆分
    memory_method = db.Column(db.Text)      # 趣味联想记忆法
    grade = db.Column(db.Integer, nullable=False, index=True)
    unit = db.Column(db.Integer, nullable=False, index=True)
    book_version = db.Column(db.String(50), default='PEP')
    audio_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联关系
    study_records = db.relationship('StudyRecord', backref='word', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Word {self.word}>'
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'word': self.word,
            'chinese_meaning': self.chinese_meaning,
            'phonetic': self.phonetic,
            'phonics_breakdown': self.phonics_breakdown,
            'memory_method': self.memory_method,
            'grade': self.grade,
            'unit': self.unit,
            'book_version': self.book_version,
            'audio_url': self.audio_url,
            'created_at': self.created_at.isoformat() if self.created_at and hasattr(self.created_at, 'isoformat') else str(self.created_at) if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at and hasattr(self.updated_at, 'isoformat') else str(self.updated_at) if self.updated_at else None
        }
    
    @staticmethod
    def get_words_by_grade_unit(grade, unit=None):
        """根据年级和单元获取单词"""
        query = Word.query.filter_by(grade=grade)
        if unit is not None:
            query = query.filter_by(unit=unit)
        return query.order_by(Word.unit, Word.id).all()
    
    @staticmethod
    def search_words(keyword):
        """搜索单词"""
        return Word.query.filter(
            db.or_(
                Word.word.contains(keyword),
                Word.chinese_meaning.contains(keyword)
            )
        ).all()

# 创建索引以优化查询性能
db.Index('idx_words_grade_unit', Word.grade, Word.unit)