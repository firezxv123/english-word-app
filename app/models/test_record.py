from datetime import datetime
from app import db
import json

class TestRecord(db.Model):
    """测验记录模型"""
    __tablename__ = 'test_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    test_type = db.Column(db.String(20), nullable=False)  # cn_to_en, en_to_cn
    total_questions = db.Column(db.Integer, nullable=False)
    correct_answers = db.Column(db.Integer, nullable=False, default=0)
    test_duration = db.Column(db.Integer)  # 测试时长（秒）
    wrong_words = db.Column(db.Text)  # JSON格式存储错题单词IDs
    grade = db.Column(db.Integer)
    unit = db.Column(db.Integer)
    tested_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    __table_args__ = (
        db.Index('idx_test_records_user_date', 'user_id', 'tested_at'),
    )
    
    def __repr__(self):
        return f'<TestRecord user:{self.user_id} type:{self.test_type} score:{self.get_score()}%>'
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'test_type': self.test_type,
            'test_type_name': self.get_test_type_name(),
            'total_questions': self.total_questions,
            'correct_answers': self.correct_answers,
            'score': self.get_score(),
            'test_duration': self.test_duration,
            'wrong_word_ids': self.get_wrong_word_ids(),
            'grade': self.grade,
            'unit': self.unit,
            'tested_at': self.tested_at.isoformat() if self.tested_at and hasattr(self.tested_at, 'isoformat') else str(self.tested_at) if self.tested_at else None
        }
    
    def get_score(self):
        """计算得分百分比"""
        if self.total_questions == 0:
            return 0
        return round((self.correct_answers / self.total_questions) * 100, 1)
    
    def get_test_type_name(self):
        """获取测试类型中文名称"""
        type_names = {
            'cn_to_en': '中译英',
            'en_to_cn': '英译中'
        }
        return type_names.get(self.test_type, self.test_type)
    
    def get_wrong_word_ids(self):
        """获取错题单词ID列表"""
        if not self.wrong_words:
            return []
        try:
            return json.loads(self.wrong_words)
        except (json.JSONDecodeError, TypeError):
            return []
    
    def set_wrong_word_ids(self, word_ids):
        """设置错题单词ID列表"""
        self.wrong_words = json.dumps(word_ids) if word_ids else None
    
    def get_wrong_words(self):
        """获取错题单词对象列表"""
        from app.models.word import Word
        
        word_ids = self.get_wrong_word_ids()
        if not word_ids:
            return []
        
        return Word.query.filter(Word.id.in_(word_ids)).all()
    
    @staticmethod
    def create_test_record(user_id, test_type, total_questions, correct_answers, 
                          test_duration, wrong_word_ids=None, grade=None, unit=None):
        """创建测验记录"""
        record = TestRecord(
            user_id=user_id,
            test_type=test_type,
            total_questions=total_questions,
            correct_answers=correct_answers,
            test_duration=test_duration,
            grade=grade,
            unit=unit
        )
        
        if wrong_word_ids:
            record.set_wrong_word_ids(wrong_word_ids)
        
        db.session.add(record)
        db.session.commit()
        return record
    
    @staticmethod
    def get_user_test_stats(user_id, days=30):
        """获取用户测验统计"""
        from sqlalchemy import func
        from datetime import timedelta
        
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        records = TestRecord.query.filter(
            TestRecord.user_id == user_id,
            TestRecord.tested_at >= start_date
        ).all()
        
        if not records:
            return {
                'total_tests': 0,
                'average_score': 0,
                'total_questions': 0,
                'total_correct': 0,
                'test_types': {}
            }
        
        total_tests = len(records)
        total_questions = sum(r.total_questions for r in records)
        total_correct = sum(r.correct_answers for r in records)
        average_score = (total_correct / total_questions * 100) if total_questions > 0 else 0
        
        # 按测试类型统计
        test_types = {}
        for record in records:
            if record.test_type not in test_types:
                test_types[record.test_type] = {
                    'count': 0,
                    'total_questions': 0,
                    'total_correct': 0,
                    'average_score': 0
                }
            
            test_types[record.test_type]['count'] += 1
            test_types[record.test_type]['total_questions'] += record.total_questions
            test_types[record.test_type]['total_correct'] += record.correct_answers
        
        # 计算各类型平均分
        for test_type in test_types:
            stats = test_types[test_type]
            if stats['total_questions'] > 0:
                stats['average_score'] = round(stats['total_correct'] / stats['total_questions'] * 100, 1)
        
        return {
            'total_tests': total_tests,
            'average_score': round(average_score, 1),
            'total_questions': total_questions,
            'total_correct': total_correct,
            'test_types': test_types
        }