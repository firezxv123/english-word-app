# 验证器模块

import re
from app.utils.constants import PATTERNS, SUPPORTED_GRADES

def validate_username(username):
    """验证用户名"""
    if not username:
        return False, "用户名不能为空"
    
    if len(username) < 2 or len(username) > 20:
        return False, "用户名长度应为2-20个字符"
    
    if not re.match(PATTERNS['username'], username):
        return False, "用户名只能包含中文、英文和数字"
    
    return True, None

def validate_grade(grade):
    """验证年级"""
    try:
        grade_int = int(grade)
        if grade_int not in SUPPORTED_GRADES:
            return False, f"年级必须在{min(SUPPORTED_GRADES)}-{max(SUPPORTED_GRADES)}之间"
        return True, None
    except (ValueError, TypeError):
        return False, "年级必须是有效的数字"

def validate_unit(unit):
    """验证单元"""
    try:
        unit_int = int(unit)
        if unit_int < 1:
            return False, "单元必须是正整数"
        return True, None
    except (ValueError, TypeError):
        return False, "单元必须是有效的数字"

def validate_mastery_level(level):
    """验证掌握程度"""
    try:
        level_int = int(level)
        if level_int < 1 or level_int > 5:
            return False, "掌握程度必须在1-5之间"
        return True, None
    except (ValueError, TypeError):
        return False, "掌握程度必须是有效的数字"

def validate_word(word):
    """验证单词格式"""
    if not word:
        return False, "单词不能为空"
    
    word = word.strip()
    if len(word) < 1 or len(word) > 100:
        return False, "单词长度应为1-100个字符"
    
    if not re.match(PATTERNS['word'], word):
        return False, "单词只能包含英文字母、空格、连字符和撇号"
    
    return True, None

def validate_chinese_meaning(meaning):
    """验证中文含义"""
    if not meaning:
        return False, "中文含义不能为空"
    
    meaning = meaning.strip()
    if len(meaning) < 1 or len(meaning) > 500:
        return False, "中文含义长度应为1-500个字符"
    
    return True, None

def validate_phonetic(phonetic):
    """验证音标格式"""
    if not phonetic:
        return True, None  # 音标是可选的
    
    phonetic = phonetic.strip()
    if len(phonetic) > 200:
        return False, "音标长度不能超过200个字符"
    
    # 简单验证音标格式（可以更复杂）
    if phonetic.startswith('/') and phonetic.endswith('/'):
        return True, None
    elif phonetic.startswith('[') and phonetic.endswith(']'):
        return True, None
    else:
        return False, "音标格式应为 /.../ 或 [...] 格式"

def validate_email(email):
    """验证邮箱格式"""
    if not email:
        return False, "邮箱不能为空"
    
    if not re.match(PATTERNS['email'], email):
        return False, "邮箱格式不正确"
    
    return True, None

def validate_phone(phone):
    """验证手机号格式"""
    if not phone:
        return False, "手机号不能为空"
    
    if not re.match(PATTERNS['phone'], phone):
        return False, "手机号格式不正确"
    
    return True, None

def validate_test_type(test_type):
    """验证测验类型"""
    valid_types = ['cn_to_en', 'en_to_cn']
    if test_type not in valid_types:
        return False, f"测验类型必须是 {', '.join(valid_types)} 之一"
    
    return True, None

def validate_question_count(count):
    """验证题目数量"""
    try:
        count_int = int(count)
        if count_int < 1 or count_int > 50:
            return False, "题目数量必须在1-50之间"
        return True, None
    except (ValueError, TypeError):
        return False, "题目数量必须是有效的数字"

def validate_file_extension(filename, allowed_extensions):
    """验证文件扩展名"""
    if not filename:
        return False, "文件名不能为空"
    
    if '.' not in filename:
        return False, "文件必须有扩展名"
    
    ext = filename.rsplit('.', 1)[1].lower()
    if ext not in allowed_extensions:
        return False, f"只支持 {', '.join(allowed_extensions)} 格式的文件"
    
    return True, None

def validate_url(url):
    """验证URL格式"""
    if not url:
        return True, None  # URL是可选的
    
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    if not url_pattern.match(url):
        return False, "URL格式不正确"
    
    return True, None

def validate_word_data(data):
    """验证完整的单词数据"""
    errors = []
    
    # 验证必需字段
    required_fields = ['word', 'chinese_meaning', 'grade', 'unit']
    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"缺少必需字段: {field}")
    
    if errors:
        return False, errors
    
    # 验证各个字段
    validators = [
        ('word', validate_word),
        ('chinese_meaning', validate_chinese_meaning),
        ('grade', validate_grade),
        ('unit', validate_unit),
        ('phonetic', validate_phonetic),
        ('audio_url', validate_url)
    ]
    
    for field, validator in validators:
        if field in data and data[field]:
            is_valid, error = validator(data[field])
            if not is_valid:
                errors.append(f"{field}: {error}")
    
    if errors:
        return False, errors
    
    return True, None

def validate_user_data(data):
    """验证用户数据"""
    errors = []
    
    # 验证必需字段
    required_fields = ['username', 'grade']
    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"缺少必需字段: {field}")
    
    if errors:
        return False, errors
    
    # 验证用户名
    is_valid, error = validate_username(data['username'])
    if not is_valid:
        errors.append(f"用户名: {error}")
    
    # 验证年级
    is_valid, error = validate_grade(data['grade'])
    if not is_valid:
        errors.append(f"年级: {error}")
    
    # 验证可选字段
    if 'current_unit' in data and data['current_unit']:
        is_valid, error = validate_unit(data['current_unit'])
        if not is_valid:
            errors.append(f"当前单元: {error}")
    
    if errors:
        return False, errors
    
    return True, None