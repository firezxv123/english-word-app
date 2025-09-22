from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import config
import os

# 全局扩展对象
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()

def create_app(config_name=None):
    """创建Flask应用工厂函数"""
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')
    
    # 创建Flask应用实例
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    
    # 注册蓝图
    from app.routes.views import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from app.routes.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    # 创建必要的目录
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    if not os.path.exists(app.config['AUDIO_FOLDER']):
        os.makedirs(app.config['AUDIO_FOLDER'])
    
    return app