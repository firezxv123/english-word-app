from flask import Blueprint

# 创建API蓝图
api = Blueprint('api', __name__)

# 导入所有API路由
from . import words, study, test, users, export, cache, maintenance