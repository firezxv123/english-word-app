#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 简单快速测试
import os
import sys
sys.path.append('/d/qodercode')

from app import create_app, db
from app.models.word import Word
from app.models.user import User

def setup_test_data():
    """设置测试数据"""
    app = create_app()
    
    with app.app_context():
        # 创建测试用户
        if User.query.count() == 0:
            user = User(username="测试学生", grade=3)
            db.session.add(user)
            print("创建测试用户")
        
        # 创建测试词汇
        if Word.query.count() == 0:
            test_words = [
                Word(word='hello', chinese_meaning='你好', grade=3, unit=1),
                Word(word='goodbye', chinese_meaning='再见', grade=3, unit=1),
                Word(word='apple', chinese_meaning='苹果', grade=3, unit=1),
                Word(word='book', chinese_meaning='书', grade=3, unit=1),
                Word(word='cat', chinese_meaning='猫', grade=3, unit=1),
                Word(word='dog', chinese_meaning='狗', grade=3, unit=1),
                Word(word='red', chinese_meaning='红色', grade=3, unit=1),
                Word(word='blue', chinese_meaning='蓝色', grade=3, unit=1),
            ]
            
            for word in test_words:
                db.session.add(word)
            
            print(f"创建了 {len(test_words)} 个测试词汇")
        
        db.session.commit()
        
        # 验证数据
        words = Word.query.limit(3).all()
        print("\n词汇示例:")
        for word in words:
            print(f"  {word.word} -> {word.chinese_meaning}")

if __name__ == "__main__":
    setup_test_data()