# 应用常量定义

# 应用信息
APP_NAME = '小学英语单词复习应用'
APP_VERSION = '1.0.0'
APP_DESCRIPTION = '专为小学3-6年级学生设计的人教版PEP教材英语单词复习背诵应用'

# 支持的年级
SUPPORTED_GRADES = [3, 4, 5, 6]
GRADE_NAMES = {
    3: '三年级',
    4: '四年级',
    5: '五年级',
    6: '六年级'
}

# 年级单元结构（2024年新版人教版PEP教材标准）
# 每个年级分为上下册，每册6个单元
GRADE_UNITS = {
    3: {
        'upper_semester': list(range(1, 7)),  # 上册：1-6单元
        'lower_semester': list(range(7, 13)),  # 下册：7-12单元
        'total_units': 12
    },
    4: {
        'upper_semester': list(range(1, 7)),  # 上册：1-6单元
        'lower_semester': list(range(7, 13)),  # 下册：7-12单元
        'total_units': 12
    },
    5: {
        'upper_semester': list(range(1, 7)),  # 上册：1-6单元
        'lower_semester': list(range(7, 13)),  # 下册：7-12单元
        'total_units': 12
    },
    6: {
        'upper_semester': list(range(1, 7)),  # 上册：1-6单元
        'lower_semester': list(range(7, 11)),  # 下册：7-10单元（六年级下册较少）
        'total_units': 10
    }
}

# 获取年级所有单元的函数
def get_grade_all_units(grade):
    """获取指定年级的所有单元"""
    if grade not in GRADE_UNITS:
        return []
    grade_info = GRADE_UNITS[grade]
    return grade_info['upper_semester'] + grade_info['lower_semester']

# 判断单元是否属于上册还是下册
def get_semester_info(grade, unit):
    """获取单元所属学期信息"""
    if grade not in GRADE_UNITS:
        return None
    
    grade_info = GRADE_UNITS[grade]
    if unit in grade_info['upper_semester']:
        return 'upper_semester'
    elif unit in grade_info['lower_semester']:
        return 'lower_semester'
    else:
        return None

# 掌握程度定义
MASTERY_LEVELS = {
    1: '初次接触',
    2: '有印象',
    3: '基本认识',
    4: '较熟练',
    5: '完全掌握'
}

# 测验类型
TEST_TYPES = {
    'cn_to_en': '中译英',
    'en_to_cn': '英译中'
}

# 教材版本
BOOK_VERSIONS = {
    'PEP': '人教版PEP',
    '外研版': '外研版',
    '牛津版': '牛津版'
}

# API响应状态码
API_SUCCESS = 200
API_CREATED = 201
API_BAD_REQUEST = 400
API_UNAUTHORIZED = 401
API_FORBIDDEN = 403
API_NOT_FOUND = 404
API_INTERNAL_ERROR = 500

# 分页设置
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# 缓存键前缀
CACHE_PREFIX = 'wordapp:'
USER_CACHE_KEY = CACHE_PREFIX + 'user:{}'
WORD_CACHE_KEY = CACHE_PREFIX + 'word:{}'
PROGRESS_CACHE_KEY = CACHE_PREFIX + 'progress:{}:{}'

# 文件上传设置
ALLOWED_EXTENSIONS = {'txt', 'csv', 'json', 'xlsx'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

# 导入导出格式
IMPORT_FORMATS = ['csv', 'json', 'xlsx']
EXPORT_FORMATS = ['csv', 'json']

# CSV字段映射
CSV_FIELD_MAPPING = {
    'word': '单词',
    'chinese_meaning': '中文含义',
    'phonetic': '音标',
    'phonics_breakdown': '拼读拆分',
    'memory_method': '记忆方法',
    'grade': '年级',
    'unit': '单元',
    'book_version': '教材版本',
    'audio_url': '音频链接'
}

# 默认配置
DEFAULT_QUESTION_COUNT = 10
MAX_QUESTION_COUNT = 50
MIN_QUESTION_COUNT = 5

# 学习会话设置
SESSION_TIMEOUT = 3600  # 1小时
MAX_WORDS_PER_SESSION = 50

# 测验会话设置
TEST_SESSION_TIMEOUT = 7200  # 2小时
MAX_TEST_DURATION = 1800  # 30分钟

# 统计时间范围
STATS_TIME_RANGES = {
    'daily': 1,
    'weekly': 7,
    'monthly': 30,
    'yearly': 365
}

# 错误消息
ERROR_MESSAGES = {
    'user_not_found': '用户不存在',
    'word_not_found': '单词不存在',
    'invalid_grade': '年级必须在3-6之间',
    'invalid_unit': '单元必须是正整数',
    'invalid_mastery_level': '掌握程度必须在1-5之间',
    'invalid_test_type': '无效的测验类型',
    'username_exists': '用户名已存在',
    'username_invalid': '用户名只能包含中文、英文和数字，长度2-20个字符',
    'test_not_found': '测验不存在或已过期',
    'test_completed': '测验已完成',
    'no_words_found': '没有找到符合条件的单词',
    'import_format_error': '不支持的导入格式',
    'file_too_large': '文件大小超过限制',
    'csv_format_error': 'CSV格式错误',
    'json_format_error': 'JSON格式错误'
}

# 成功消息
SUCCESS_MESSAGES = {
    'user_created': '用户创建成功',
    'user_updated': '用户信息更新成功',
    'user_deleted': '用户删除成功',
    'word_created': '单词创建成功',
    'word_updated': '单词更新成功',
    'word_deleted': '单词删除成功',
    'progress_recorded': '学习进度记录成功',
    'test_generated': '测验生成成功',
    'test_completed': '测验完成',
    'import_success': '数据导入成功',
    'export_success': '数据导出成功'
}

# 音频文件支持的格式
AUDIO_FORMATS = ['mp3', 'wav', 'ogg', 'm4a']

# 图片文件支持的格式
IMAGE_FORMATS = ['jpg', 'jpeg', 'png', 'gif', 'webp']

# 正则表达式模式
PATTERNS = {
    'username': r'^[\u4e00-\u9fa5a-zA-Z0-9]{2,20}$',
    'email': r'^[^\s@]+@[^\s@]+\.[^\s@]+$',
    'phone': r'^1[3-9]\d{9}$',
    'word': r'^[a-zA-Z\s\-\']+$',
    'phonetic': r'^\/.*\/$'
}

# 默认设置
DEFAULTS = {
    'grade': 3,
    'unit': 1,
    'mastery_level': 1,
    'test_type': 'cn_to_en',
    'question_count': 10,
    'book_version': 'PEP'
}

# 系统配置
SYSTEM_CONFIG = {
    'auto_save_interval': 30,  # 自动保存间隔（秒）
    'session_cleanup_interval': 3600,  # 会话清理间隔（秒）
    'max_login_attempts': 5,  # 最大登录尝试次数
    'password_min_length': 6,  # 密码最小长度
    'backup_retention_days': 30,  # 备份保留天数
}