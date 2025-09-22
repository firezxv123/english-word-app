#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
参数处理工具
"""

def safe_int(value, default=None):
    """安全地将值转换为int，处理空字符串和None"""
    if value is None or value == '':
        return default
    
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def safe_get_int_param(request_args, param_name, default=None):
    """从请求参数中安全获取int值"""
    value = request_args.get(param_name)
    return safe_int(value, default)

def safe_get_form_int(request_form, param_name, default=None):
    """从表单中安全获取int值"""
    value = request_form.get(param_name)
    return safe_int(value, default)