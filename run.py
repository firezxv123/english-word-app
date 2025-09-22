#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask_migrate import upgrade
from app import create_app, db

app = create_app()

@app.cli.command()
def deploy():
    """运行部署任务"""
    # 迁移数据库到最新版本
    upgrade()

@app.cli.command()
def init_db():
    """初始化数据库"""
    with app.app_context():
        # 创建所有表
        db.create_all()
        
        # 导入初始数据
        from app.services.data_import import DataImportService
        
        # 检查是否已有词库数据
        from app.models.word import Word
        if Word.query.count() == 0:
            print("正在初始化词库数据...")
            
            # 加载完整词库数据
            sample_words = get_sample_words()
            
            try:
                result = DataImportService.import_from_json(sample_words)
                if result['success']:
                    print(f"成功导入 {result['imported_count']} 个单词")
                    print(f"涵盖3-6年级，每年级12个单元")
                else:
                    print(f"导入失败: {result['error']}")
            except Exception as e:
                print(f"导入数据时出错: {str(e)}")
        else:
            print(f"词库数据已存在，当前有 {Word.query.count()} 个单词")
        
        print("数据库初始化完成")

def get_sample_words():
    """获取完整的词库数据 - 3-6年级，每年级12个单元"""
    from complete_words_data import get_all_words
    return get_all_words()

if __name__ == '__main__':
    # 获取配置
    config_name = os.environ.get('FLASK_CONFIG', 'development')
    
    app = create_app(config_name)
    
    # 如果是开发环境，启用调试模式
    if config_name == 'development':
        app.run(host='0.0.0.0', port=3000, debug=True)
    else:
        app.run(host='0.0.0.0', port=3000)