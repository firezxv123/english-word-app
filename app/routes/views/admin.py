#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, request, jsonify, send_file
from app.routes.views import main
from app.utils.error_handler import ErrorHandler
from app.utils.param_helpers import safe_get_int_param
import os
import logging

@main.route('/admin/logs')
def admin_logs():
    """管理员日志查看页面"""
    return render_template('admin/logs.html')

@main.route('/admin/logs/api')
def get_logs():
    """获取日志数据API"""
    try:
        log_file = 'app.log'
        lines = safe_get_int_param(request.args, 'lines', 100)
        level = request.args.get('level', 'all')
        
        if not os.path.exists(log_file):
            return jsonify({
                'success': True,
                'data': [],
                'message': '日志文件不存在'
            })
        
        logs = []
        with open(log_file, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
            # 获取最后N行
            recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
            
            for line in recent_lines:
                line = line.strip()
                if not line:
                    continue
                
                # 解析日志级别
                if level != 'all':
                    if level.upper() not in line:
                        continue
                
                logs.append(line)
        
        return jsonify({
            'success': True,
            'data': logs,
            'count': len(logs)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@main.route('/admin/logs/download')
def download_logs():
    """下载日志文件"""
    try:
        log_file = 'app.log'
        
        if not os.path.exists(log_file):
            return jsonify({
                'success': False,
                'error': '日志文件不存在'
            }), 404
        
        return send_file(log_file, as_attachment=True, download_name='app.log')
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@main.route('/admin/logs/clear', methods=['POST'])
def clear_logs():
    """清空日志文件"""
    try:
        log_file = 'app.log'
        
        if os.path.exists(log_file):
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write('')
        
        ErrorHandler.log_system_event('admin_action', '日志文件已清空')
        
        return jsonify({
            'success': True,
            'message': '日志文件已清空'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@main.route('/admin/system/info')
def system_info():
    """系统信息页面"""
    import sys
    import platform
    from datetime import datetime
    from app.models.word import Word
    from app.models.user import User
    
    try:
        system_info = {
            'python_version': sys.version,
            'platform': platform.platform(),
            'start_time': datetime.now().isoformat(),
            'word_count': Word.query.count(),
            'user_count': User.query.count(),
            'log_file_size': os.path.getsize('app.log') if os.path.exists('app.log') else 0
        }
        
        return render_template('admin/system_info.html', system_info=system_info)
        
    except Exception as e:
        ErrorHandler.log_system_event('admin_error', f'获取系统信息失败: {str(e)}', 'error')
        return render_template('admin/system_info.html', system_info={}, error=str(e))