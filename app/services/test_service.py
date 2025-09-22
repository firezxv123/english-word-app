from app.models.test_record import TestRecord
from app.models.user import User
from app.models.test_record import TestRecord
from app.services.word_service import WordService
from app import db
import random
import uuid
from datetime import datetime

class TestService:
    """测验服务类"""
    
    # 临时存储测验会话（实际项目中应使用Redis等缓存）
    _test_sessions = {}
    
    @staticmethod
    def generate_test(user_id, test_type, grade=None, unit=None, question_count=10):
        """生成测验"""
        # 安全处理参数
        if question_count is None or question_count <= 0:
            question_count = 10
        
        user = User.query.get(user_id)
        if not user:
            return None, "用户不存在"
        
        if test_type not in ['cn_to_en', 'en_to_cn']:
            return None, "无效的测验类型"
        
        # 获取测验单词
        if grade and unit:
            words = WordService.get_words_by_criteria(grade=grade, unit=unit)
        elif grade:
            words = WordService.get_words_by_criteria(grade=grade)
        else:
            words = WordService.get_words_by_criteria(grade=user.grade)
        
        if len(words) < question_count:
            question_count = len(words)
        
        if question_count == 0:
            return None, "没有找到符合条件的单词"
        
        # 随机选择单词
        test_words = random.sample(words, question_count)
        
        # 生成测验ID
        test_id = str(uuid.uuid4())
        
        # 生成题目
        questions = []
        for i, word in enumerate(test_words):
            if test_type == 'cn_to_en':
                # 中译英：显示中文，选择英文答案
                question = TestService._generate_cn_to_en_question(word, words)
            else:
                # 英译中：显示英文，选择中文答案
                question = TestService._generate_en_to_cn_question(word, words)
            
            question['id'] = i + 1
            questions.append(question)
        
        # 保存测验会话
        session_data = {
            'test_id': test_id,
            'user_id': user_id,
            'test_type': test_type,
            'grade': grade,
            'unit': unit,
            'questions': questions,
            'answers': {},
            'start_time': datetime.now(),
            'status': 'started'
        }
        
        TestService._test_sessions[test_id] = session_data
        
        return {
            'test_id': test_id,
            'test_type': test_type,
            'test_type_name': '中译英' if test_type == 'cn_to_en' else '英译中',
            'total_questions': len(questions),
            'questions': [TestService._format_question_for_client(q) for q in questions]
        }, None
    
    @staticmethod
    def _generate_cn_to_en_question(correct_word, all_words):
        """生成中译英题目"""
        # 获取其他单词作为干扰项
        other_words = [w for w in all_words if w.id != correct_word.id]
        distractors = random.sample(other_words, min(3, len(other_words)))
        
        # 组合选项
        options = [correct_word] + distractors
        random.shuffle(options)
        
        return {
            'word_id': correct_word.id,
            'question_text': correct_word.chinese_meaning,
            'question_type': 'cn_to_en',
            'options': [{'value': w.word, 'text': w.word} for w in options],
            'correct_answer': correct_word.word
        }
    
    @staticmethod
    def _generate_en_to_cn_question(correct_word, all_words):
        """生成英译中题目"""
        # 获取其他单词作为干扰项
        other_words = [w for w in all_words if w.id != correct_word.id]
        distractors = random.sample(other_words, min(3, len(other_words)))
        
        # 组合选项
        options = [correct_word] + distractors
        random.shuffle(options)
        
        return {
            'word_id': correct_word.id,
            'question_text': correct_word.word,
            'question_type': 'en_to_cn',
            'options': [{'value': w.chinese_meaning, 'text': w.chinese_meaning} for w in options],
            'correct_answer': correct_word.chinese_meaning
        }
    
    @staticmethod
    def _format_question_for_client(question):
        """格式化题目给客户端"""
        return {
            'id': question['id'],
            'question_text': question['question_text'],
            'question_type': question['question_type'],
            'options': question['options']
        }
    
    @staticmethod
    def submit_answer(test_id, question_id, answer):
        """提交答案"""
        if test_id not in TestService._test_sessions:
            return None, "测验不存在或已过期"
        
        session = TestService._test_sessions[test_id]
        
        if session['status'] != 'started':
            return None, "测验已结束"
        
        # 保存答案
        session['answers'][str(question_id)] = answer
        
        return {'success': True}, None
    
    @staticmethod
    def finish_test(test_id):
        """完成测验并计算结果"""
        if test_id not in TestService._test_sessions:
            return None, "测验不存在或已过期"
        
        session = TestService._test_sessions[test_id]
        
        if session['status'] != 'started':
            return None, "测验已结束"
        
        # 计算结果
        questions = session['questions']
        answers = session['answers']
        
        correct_count = 0
        wrong_word_ids = []
        
        for question in questions:
            question_id = str(question['id'])
            user_answer = answers.get(question_id, '')
            correct_answer = question['correct_answer']
            
            if user_answer:
                user_clean = user_answer.strip().lower()
                correct_clean = correct_answer.strip().lower()
                
                is_correct = user_clean == correct_clean
                
                if is_correct:
                    correct_count += 1
                else:
                    wrong_word_ids.append(question['word_id'])
            else:
                wrong_word_ids.append(question['word_id'])

        
        # 计算测试时长
        end_time = datetime.now()
        duration = int((end_time - session['start_time']).total_seconds())
        
        # 保存测验记录到数据库
        test_record = TestRecord.create_test_record(
            user_id=session['user_id'],
            test_type=session['test_type'],
            total_questions=len(questions),
            correct_answers=correct_count,
            test_duration=duration,
            wrong_word_ids=wrong_word_ids,
            grade=session['grade'],
            unit=session['unit']
        )
        
        # 更新会话状态
        session['status'] = 'completed'
        session['result'] = test_record.to_dict()
        
        return test_record.to_dict(), None
    
    @staticmethod
    def get_test_result(test_id):
        """获取测验结果"""
        if test_id not in TestService._test_sessions:
            return None, "测验不存在或已过期"
        
        session = TestService._test_sessions[test_id]
        
        if session['status'] != 'completed':
            return None, "测验尚未完成"
        
        result = session['result']
        
        # 获取错题详情
        if result['wrong_word_ids']:
            wrong_words = WordService.get_words_by_criteria()
            wrong_words = [w for w in wrong_words if w.id in result['wrong_word_ids']]
            result['wrong_words'] = [w.to_dict() for w in wrong_words]
        else:
            result['wrong_words'] = []
        
        return result, None
    
    @staticmethod
    def get_user_test_history(user_id, limit=10):
        """获取用户测验历史"""
        # 安全处理limit参数
        if limit is None or limit <= 0:
            limit = 10
        
        user = User.query.get(user_id)
        if not user:
            return None, "用户不存在"
        
        records = TestRecord.query.filter_by(user_id=user_id)\
            .order_by(TestRecord.tested_at.desc())\
            .limit(limit).all()
        
        return [record.to_dict() for record in records], None
    
    @staticmethod
    def get_test_statistics(user_id):
        """获取测验统计"""
        user = User.query.get(user_id)
        if not user:
            return None, "用户不存在"
        
        # 最近30天的统计
        stats_30days = TestRecord.get_user_test_stats(user_id, days=30)
        
        # 最近7天的统计
        stats_7days = TestRecord.get_user_test_stats(user_id, days=7)
        
        # 获取最近的测验记录用于趋势分析
        recent_tests = TestRecord.query.filter_by(user_id=user_id)\
            .order_by(TestRecord.tested_at.desc())\
            .limit(10).all()
        
        return {
            'user': user.to_dict(),
            'stats_30days': stats_30days,
            'stats_7days': stats_7days,
            'recent_tests': [t.to_dict() for t in recent_tests]
        }, None
    
    @staticmethod
    def retry_wrong_words(user_id, original_test_id):
        """重新测验错题"""
        # 从数据库获取原始测验记录
        original_record = TestRecord.query.filter_by(user_id=user_id).filter(
            TestRecord.id == original_test_id
        ).first()
        
        if not original_record:
            return None, "原始测验记录不存在"
        
        wrong_word_ids = original_record.get_wrong_word_ids()
        if not wrong_word_ids:
            return None, "没有错题需要重新测验"
        
        # 获取错题单词
        wrong_words = WordService.get_words_by_criteria()
        wrong_words = [w for w in wrong_words if w.id in wrong_word_ids]
        
        if not wrong_words:
            return None, "错题单词已被删除"
        
        # 生成新的测验
        test_id = str(uuid.uuid4())
        
        # 生成题目
        questions = []
        for i, word in enumerate(wrong_words):
            if original_record.test_type == 'cn_to_en':
                question = TestService._generate_cn_to_en_question(word, wrong_words)
            else:
                question = TestService._generate_en_to_cn_question(word, wrong_words)
            
            question['id'] = i + 1
            questions.append(question)
        
        # 保存测验会话
        session_data = {
            'test_id': test_id,
            'user_id': user_id,
            'test_type': original_record.test_type,
            'grade': original_record.grade,
            'unit': original_record.unit,
            'questions': questions,
            'answers': {},
            'start_time': datetime.now(),
            'status': 'started',
            'is_retry': True,
            'original_test_id': original_test_id
        }
        
        TestService._test_sessions[test_id] = session_data
        
        return {
            'test_id': test_id,
            'test_type': original_record.test_type,
            'test_type_name': original_record.get_test_type_name(),
            'total_questions': len(questions),
            'is_retry': True,
            'original_score': original_record.get_score(),
            'questions': [TestService._format_question_for_client(q) for q in questions]
        }, None
    
    @staticmethod
    def cleanup_expired_sessions(hours=2):
        """清理过期的测验会话"""
        current_time = datetime.now()
        expired_sessions = []
        
        for test_id, session in TestService._test_sessions.items():
            if (current_time - session['start_time']).total_seconds() > hours * 3600:
                expired_sessions.append(test_id)
        
        for test_id in expired_sessions:
            del TestService._test_sessions[test_id]
        
        return len(expired_sessions)