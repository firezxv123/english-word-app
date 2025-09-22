from flask import render_template, request, redirect, url_for, flash, jsonify
from app.routes.views import main
from app.models.user import User
from app.services.study_service import StudyService
from app.services.word_service import WordService
from app.utils.param_helpers import safe_get_int_param

@main.route('/study/<int:user_id>')
def study_page(user_id):
    """学习主页"""
    user = User.query.get_or_404(user_id)
    
    # 获取用户年级的所有单元
    units = WordService.get_grade_units(user.grade)
    
    # 获取推荐学习的单词
    recommended_words, error = StudyService.get_recommended_words(user_id, 5)
    if error:
        recommended_words = []
    
    return render_template('study/index.html',
                         user=user,
                         units=units,
                         recommended_words=recommended_words)

@main.route('/study/<int:user_id>/start')
def start_study(user_id):
    """开始学习"""
    user = User.query.get_or_404(user_id)
    
    grade = safe_get_int_param(request.args, 'grade', user.grade)
    unit = safe_get_int_param(request.args, 'unit')
    
    # 验证参数
    if not grade or grade <= 0:
        grade = user.grade
    
    # 开始学习会话
    session_data, error = StudyService.start_study_session(user_id, grade, unit)
    
    if error:
        flash(f'开始学习失败：{error}', 'error')
        return redirect(url_for('main.study_page', user_id=user_id))
    
    return render_template('study/session.html',
                         user=user,
                         session=session_data)

@main.route('/study/<int:user_id>/word/<int:word_id>')
def study_word(user_id, word_id):
    """学习单词详情页"""
    user = User.query.get_or_404(user_id)
    word = WordService.get_word_by_id(word_id)
    
    if not word:
        flash('单词不存在', 'error')
        return redirect(url_for('main.study_page', user_id=user_id))
    
    # 获取用户对这个单词的学习记录
    from app.models.study_record import StudyRecord
    study_record = StudyRecord.query.filter_by(user_id=user_id, word_id=word_id).first()
    
    return render_template('study/word_detail.html',
                         user=user,
                         word=word,
                         study_record=study_record)

@main.route('/study/<int:user_id>/progress')
def study_progress(user_id):
    """学习进度页面"""
    user = User.query.get_or_404(user_id)
    
    grade = safe_get_int_param(request.args, 'grade')
    unit = safe_get_int_param(request.args, 'unit')
    
    # 获取学习进度
    progress_data, error = StudyService.get_study_progress(user_id, grade, unit)
    
    if error:
        flash(f'获取学习进度失败：{error}', 'error')
        return redirect(url_for('main.study_page', user_id=user_id))
    
    # 获取学习统计
    stats_data, error = StudyService.get_study_statistics(user_id, 7)
    
    if error:
        stats_data = None
    
    return render_template('study/progress.html',
                         user=user,
                         progress=progress_data,
                         stats=stats_data)

@main.route('/study/<int:user_id>/review')
def study_review(user_id):
    """复习页面"""
    user = User.query.get_or_404(user_id)
    
    # 获取需要复习的单词（掌握程度<4的单词）
    from app.models.study_record import StudyRecord
    
    unmastered_records = StudyRecord.query.filter(
        StudyRecord.user_id == user_id,
        StudyRecord.mastery_level < 4
    ).order_by(StudyRecord.studied_at.asc()).limit(20).all()
    
    review_words = [record.word for record in unmastered_records if record.word]
    
    return render_template('study/review.html',
                         user=user,
                         review_words=review_words)

@main.route('/study/<int:user_id>/statistics')
def study_statistics(user_id):
    """学习统计页面"""
    user = User.query.get_or_404(user_id)
    
    days = safe_get_int_param(request.args, 'days', 30)
    
    # 获取详细统计数据
    stats_data, error = StudyService.get_study_statistics(user_id, days)
    
    if error:
        flash(f'获取统计数据失败：{error}', 'error')
        return redirect(url_for('main.study_page', user_id=user_id))
    
    # 获取掌握程度分布
    mastery_data, error = StudyService.get_mastery_distribution(user_id)
    
    if error:
        mastery_data = None
    
    return render_template('study/statistics.html',
                         user=user,
                         stats=stats_data,
                         mastery=mastery_data,
                         days=days)