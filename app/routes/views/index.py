from flask import render_template, request, redirect, url_for, flash
from app.routes.views import main
from app.models.user import User
from app.services.word_service import WordService
from app.utils.param_helpers import safe_get_int_param, safe_get_form_int

@main.route('/')
def index():
    """首页"""
    # 获取用户信息（如果有用户ID参数）
    user_id = safe_get_int_param(request.args, 'user_id')
    current_user = None
    
    if user_id:
        current_user = User.query.get(user_id)
    
    # 获取词库统计
    word_stats = WordService.get_word_statistics()
    
    # 获取所有年级
    grades = WordService.get_all_grades()
    
    return render_template('index.html', 
                         current_user=current_user,
                         word_stats=word_stats,
                         grades=grades)

@main.route('/select_user')
def select_user():
    """用户选择页面"""
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('select_user.html', users=users)

@main.route('/user/create', methods=['GET', 'POST'])
def create_user():
    """创建用户页面"""
    if request.method == 'POST':
        username = request.form.get('username')
        grade = safe_get_form_int(request.form, 'grade')
        
        if not username or not grade:
            flash('请填写完整的用户信息', 'error')
            return render_template('create_user.html')
        
        # 检查用户名是否已存在
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('用户名已存在', 'error')
            return render_template('create_user.html')
        
        # 验证年级
        if grade < 3 or grade > 6:
            flash('年级必须在3-6之间', 'error')
            return render_template('create_user.html')
        
        try:
            user = User.create_user(username, grade)
            flash(f'用户 {username} 创建成功！', 'success')
            return redirect(url_for('main.index', user_id=user.id))
        except Exception as e:
            flash(f'创建用户失败：{str(e)}', 'error')
            return render_template('create_user.html')
    
    return render_template('create_user.html')

@main.route('/dashboard/<int:user_id>')
def dashboard(user_id):
    """用户仪表板"""
    user = User.query.get_or_404(user_id)
    
    # 获取学习进度
    study_progress = user.get_study_progress()
    
    # 获取最近测验记录
    recent_tests = user.get_recent_tests(5)
    
    # 获取测验统计
    from app.models.test_record import TestRecord
    test_stats = TestRecord.get_user_test_stats(user_id, days=30)
    
    return render_template('dashboard.html',
                         user=user,
                         study_progress=study_progress,
                         recent_tests=recent_tests,
                         test_stats=test_stats)

@main.route('/maintenance')
def maintenance():
    """系统维护页面"""
    return render_template('maintenance.html')

@main.route('/words')
def word_list():
    """词库管理页面"""
    grade = safe_get_int_param(request.args, 'grade')
    unit = safe_get_int_param(request.args, 'unit')
    
    # 获取所有年级
    grades = WordService.get_all_grades()
    
    # 获取单元列表
    units = []
    if grade:
        units = WordService.get_grade_units(grade)
    
    # 获取单词列表
    words = WordService.get_words_by_criteria(grade, unit)
    
    return render_template('word_list.html',
                         words=words,
                         grades=grades,
                         units=units,
                         selected_grade=grade,
                         selected_unit=unit)

@main.route('/export')
def export_page():
    """数据导出页面"""
    return render_template('export.html')