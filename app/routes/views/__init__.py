from flask import Blueprint

# 创建视图蓝图
main = Blueprint('main', __name__)

# 导入所有视图路由
from . import index, study, test, admin, word_admin