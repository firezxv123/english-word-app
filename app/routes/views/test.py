from flask import render_template, request, redirect, url_for, flash, jsonify
from app.routes.views import main
from app.models.user import User
from app.services.test_service import TestService
from app.services.word_service import WordService
from app.utils.param_helpers import safe_get_form_int, safe_get_int_param

@main.route('/test/<int:user_id>')
def test_page(user_id):
    """测验主页"""
    user = User.query.get_or_404(user_id)
    
    # 获取用户年级的所有单元
    units = WordService.get_grade_units(user.grade)
    
    # 获取最近的测验记录
    recent_tests, error = TestService.get_user_test_history(user_id, 5)
    if error:
        recent_tests = []
    
    # 获取测验统计
    test_stats, error = TestService.get_test_statistics(user_id)
    if error:
        test_stats = None
    
    return render_template('test/index.html',
                         user=user,
                         units=units,
                         recent_tests=recent_tests,
                         test_stats=test_stats)

@main.route('/test/<int:user_id>/create')
def create_test(user_id):
    """创建测验页面"""
    user = User.query.get_or_404(user_id)
    
    # 获取用户年级的所有单元
    units = WordService.get_grade_units(user.grade)
    
    return render_template('test/create.html',
                         user=user,
                         units=units)

@main.route('/test/<int:user_id>/start', methods=['POST'])
def start_test(user_id):
    """开始测验"""
    user = User.query.get_or_404(user_id)
    
    test_type = request.form.get('test_type')
    grade = safe_get_form_int(request.form, 'grade', user.grade)
    unit = safe_get_form_int(request.form, 'unit')
    question_count = safe_get_form_int(request.form, 'question_count', 10)
    
    # 验证参数
    if not test_type:
        flash('请选择测验类型', 'error')
        return redirect(url_for('main.create_test', user_id=user_id))
    
    if question_count <= 0:
        question_count = 10
    
    # 生成测验
    test_data, error = TestService.generate_test(
        user_id, test_type, grade, unit, question_count
    )
    
    if error:
        flash(f'生成测验失败：{error}', 'error')
        return redirect(url_for('main.create_test', user_id=user_id))
    
    return render_template('test/session.html',
                         user=user,
                         test=test_data)

@main.route('/test/session/<test_id>')
def test_session(test_id):
    """测验会话页面"""
    # 从测验服务获取测验会话数据
    from app.services.test_service import TestService
    
    # 尝试从TestService的会话缓存中获取测试数据
    if test_id in TestService._test_sessions:
        session_data = TestService._test_sessions[test_id]
        
        # 获取用户信息
        user = User.query.get(session_data['user_id'])
        if not user:
            flash('用户不存在', 'error')
            return redirect(url_for('main.index'))
        
        # 构建测试数据（与generate_test返回格式一致）
        test_data = {
            'test_id': test_id,
            'test_type': session_data['test_type'],
            'test_type_name': '中译英' if session_data['test_type'] == 'cn_to_en' else '英译中',
            'total_questions': len(session_data['questions']),
            'questions': [TestService._format_question_for_client(q) for q in session_data['questions']]
        }
        
        return render_template('test/session.html',
                             user=user,
                             test=test_data)
    else:
        flash('测验会话不存在或已过期', 'error')
        return redirect(url_for('main.index'))

@main.route('/test/result/<test_id>')
def test_result(test_id):
    """测验结果页面"""
    # 获取测验结果
    result, error = TestService.get_test_result(test_id)
    
    if error:
        flash(f'获取测验结果失败：{error}', 'error')
        return redirect(url_for('main.index'))
    
    # 获取用户信息
    user = User.query.get(result['user_id'])
    
    return render_template('test/result.html',
                         user=user,
                         result=result)

@main.route('/test/<int:user_id>/history')
def test_history(user_id):
    """测验历史页面"""
    user = User.query.get_or_404(user_id)
    
    limit = safe_get_int_param(request.args, 'limit', 20)
    
    # 获取测验历史
    history, error = TestService.get_user_test_history(user_id, limit)
    
    if error:
        flash(f'获取测验历史失败：{error}', 'error')
        return redirect(url_for('main.test_page', user_id=user_id))
    
    return render_template('test/history.html',
                         user=user,
                         history=history)

@main.route('/test/<int:user_id>/statistics')
def test_statistics(user_id):
    """测验统计页面"""
    user = User.query.get_or_404(user_id)
    
    # 获取详细统计数据
    stats, error = TestService.get_test_statistics(user_id)
    
    if error:
        flash(f'获取统计数据失败：{error}', 'error')
        return redirect(url_for('main.test_page', user_id=user_id))
    
    return render_template('test/statistics.html',
                         user=user,
                         stats=stats)

@main.route('/test/<int:user_id>/retry/<int:original_test_id>')
def retry_test(user_id, original_test_id):
    """重新测验错题"""
    user = User.query.get_or_404(user_id)
    
    # 生成错题重测
    retry_data, error = TestService.retry_wrong_words(user_id, original_test_id)
    
    if error:
        flash(f'生成重测失败：{error}', 'error')
        return redirect(url_for('main.test_history', user_id=user_id))
    
    return render_template('test/session.html',
                         user=user,
                         test=retry_data)