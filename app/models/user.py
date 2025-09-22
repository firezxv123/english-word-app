from datetime import datetime
from app import db

class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True, index=True)
    grade = db.Column(db.Integer, nullable=False)
    current_unit = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关联关系
    study_records = db.relationship('StudyRecord', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    test_records = db.relationship('TestRecord', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'username': self.username,
            'grade': self.grade,
            'current_unit': self.current_unit,
            'created_at': self.created_at.isoformat() if self.created_at and hasattr(self.created_at, 'isoformat') else str(self.created_at) if self.created_at else None
        }
    
    def get_study_progress(self):
        """获取学习进度统计"""
        from app.models.study_record import StudyRecord
        
        # 总学习单词数
        total_studied = StudyRecord.query.filter_by(user_id=self.id).count()
        
        # 已掌握单词数（掌握程度>=4）
        mastered = StudyRecord.query.filter_by(user_id=self.id).filter(
            StudyRecord.mastery_level >= 4
        ).count()
        
        # 当前单元学习进度
        current_unit_studied = StudyRecord.query.join(StudyRecord.word).filter(
            StudyRecord.user_id == self.id,
            StudyRecord.word.has(grade=self.grade, unit=self.current_unit)
        ).count()
        
        return {
            'total_studied': total_studied,
            'mastered': mastered,
            'mastery_rate': round((mastered / total_studied * 100) if total_studied > 0 else 0, 1),
            'current_unit_studied': current_unit_studied
        }
    
    def get_recent_tests(self, limit=5):
        """获取最近的测验记录"""
        from app.models.test_record import TestRecord
        
        return TestRecord.query.filter_by(user_id=self.id).order_by(
            TestRecord.tested_at.desc()
        ).limit(limit).all()
    
    @staticmethod
    def create_user(username, grade):
        """创建新用户"""
        user = User(username=username, grade=grade)
        db.session.add(user)
        db.session.commit()
        return user