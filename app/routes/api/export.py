#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, jsonify, send_file, make_response
from app.routes.api import api
from app.services.export_service import ExportService
from app.services.word_service import WordService
from app.services.user_service import UserService
from app.utils.error_handler import ErrorHandler, ValidationError, NotFoundError
from app.utils.param_helpers import safe_get_int_param
from datetime import datetime
import io
import csv

@api.route('/export/words/csv', methods=['GET'])
@ErrorHandler.handle_api_error
def export_words_csv():
    """导出单词为CSV格式"""
    grade = safe_get_int_param(request.args, 'grade')
    unit = safe_get_int_param(request.args, 'unit')
    
    # 获取单词列表
    words = WordService.get_words_by_criteria(grade, unit)
    
    if not words:
        raise NotFoundError('没有找到符合条件的单词')
    
    # 导出CSV
    csv_content, error = ExportService.export_words_to_csv(words)
    
    if error:
        raise Exception(error)
    
    # 创建文件名
    filename_parts = ['words']
    if grade:
        filename_parts.append(f'grade{grade}')
    if unit:
        filename_parts.append(f'unit{unit}')
    filename_parts.append(datetime.now().strftime('%Y%m%d'))
    filename = '_'.join(filename_parts) + '.csv'
    
    # 创建响应
    output = io.StringIO(csv_content)
    mem = io.BytesIO()
    mem.write(csv_content.encode('utf-8-sig'))  # 添加BOM以支持Excel
    mem.seek(0)
    
    return send_file(
        mem,
        mimetype='text/csv',
        as_attachment=True,
        download_name=filename
    )

@api.route('/export/words/pdf', methods=['GET'])
@ErrorHandler.handle_api_error
def export_words_pdf():
    """导出单词为PDF格式"""
    grade = safe_get_int_param(request.args, 'grade')
    unit = safe_get_int_param(request.args, 'unit')
    
    # 获取单词列表
    words = WordService.get_words_by_criteria(grade, unit)
    
    if not words:
        raise NotFoundError('没有找到符合条件的单词')
    
    # 创建标题
    title_parts = ['单词列表']
    if grade:
        title_parts.append(f'{grade}年级')
    if unit:
        title_parts.append(f'第{unit}单元')
    title = ' - '.join(title_parts)
    
    # 导出PDF
    pdf_content, error = ExportService.export_words_to_pdf(words, title)
    
    if error:
        raise Exception(error)
    
    # 创建文件名
    filename_parts = ['words']
    if grade:
        filename_parts.append(f'grade{grade}')
    if unit:
        filename_parts.append(f'unit{unit}')
    filename_parts.append(datetime.now().strftime('%Y%m%d'))
    filename = '_'.join(filename_parts) + '.pdf'
    
    # 创建响应
    mem = io.BytesIO(pdf_content)
    
    return send_file(
        mem,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )

@api.route('/export/words/json', methods=['GET'])
@ErrorHandler.handle_api_error
def export_words_json():
    """导出单词为JSON格式"""
    grade = safe_get_int_param(request.args, 'grade')
    unit = safe_get_int_param(request.args, 'unit')
    formatted = request.args.get('formatted', 'true').lower() == 'true'
    
    # 获取单词列表
    words = WordService.get_words_by_criteria(grade, unit)
    
    if not words:
        raise NotFoundError('没有找到符合条件的单词')
    
    # 转换为字典列表
    words_data = [word.to_dict() for word in words]
    
    # 导出JSON
    json_content, error = ExportService.export_to_json(words_data, formatted)
    
    if error:
        raise Exception(error)
    
    # 创建文件名
    filename_parts = ['words']
    if grade:
        filename_parts.append(f'grade{grade}')
    if unit:
        filename_parts.append(f'unit{unit}')
    filename_parts.append(datetime.now().strftime('%Y%m%d'))
    filename = '_'.join(filename_parts) + '.json'
    
    # 创建响应
    response = make_response(json_content)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    
    return response

@api.route('/export/study-report/<int:user_id>/pdf', methods=['GET'])
@ErrorHandler.handle_api_error
def export_study_report_pdf(user_id):
    """导出用户学习报告为PDF格式"""
    # 获取用户信息
    user = UserService.get_user_by_id(user_id)
    if not user:
        raise NotFoundError('用户不存在')
    
    # 获取学习数据
    study_data = user.get_study_progress()
    
    # 获取测验数据
    from app.models.test_record import TestRecord
    test_data = TestRecord.get_user_test_stats(user_id, days=30)
    
    # 导出PDF
    pdf_content, error = ExportService.export_study_report_to_pdf(user, study_data, test_data)
    
    if error:
        raise Exception(error)
    
    # 创建文件名
    filename = f'study_report_{user.username}_{datetime.now().strftime("%Y%m%d")}.pdf'
    
    # 创建响应
    mem = io.BytesIO(pdf_content)
    
    return send_file(
        mem,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )

@api.route('/export/study-report/<int:user_id>/csv', methods=['GET'])
@ErrorHandler.handle_api_error
def export_study_report_csv(user_id):
    """导出用户学习报告为CSV格式"""
    # 获取用户信息
    user = UserService.get_user_by_id(user_id)
    if not user:
        raise NotFoundError('用户不存在')
    
    # 获取学习记录
    study_records = user.study_records.order_by('studied_at').all()
    
    # 创建CSV内容
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_ALL)
    
    # 写入表头
    headers = ['学习时间', '单词', '中文含义', '年级', '单元', '掌握程度']
    writer.writerow(headers)
    
    # 写入数据
    for record in study_records:
        row = [
            record.studied_at.strftime('%Y-%m-%d %H:%M:%S'),
            record.word.word,
            record.word.chinese_meaning,
            record.word.grade,
            record.word.unit,
            record.mastery_level
        ]
        writer.writerow(row)
    
    csv_content = output.getvalue()
    output.close()
    
    # 创建文件名
    filename = f'study_records_{user.username}_{datetime.now().strftime("%Y%m%d")}.csv'
    
    # 创建响应
    mem = io.BytesIO()
    mem.write(csv_content.encode('utf-8-sig'))
    mem.seek(0)
    
    return send_file(
        mem,
        mimetype='text/csv',
        as_attachment=True,
        download_name=filename
    )

@api.route('/export/formats', methods=['GET'])
@ErrorHandler.handle_api_error
def get_export_formats():
    """获取支持的导出格式"""
    formats = {
        'words': [
            {'format': 'csv', 'name': 'CSV格式', 'description': '逗号分隔值，兼容Excel'},
            {'format': 'json', 'name': 'JSON格式', 'description': '结构化数据格式'},
        ],
        'reports': [
            {'format': 'csv', 'name': 'CSV格式', 'description': '学习记录数据'}
        ]
    }
    
    # 只有安装了reportlab才支持PDF
    try:
        import reportlab
        formats['words'].append({
            'format': 'pdf', 
            'name': 'PDF格式', 
            'description': '便携式文档格式，适合打印'
        })
        formats['reports'].append({
            'format': 'pdf', 
            'name': 'PDF格式', 
            'description': '学习报告文档'
        })
    except ImportError:
        pass
    
    return jsonify({
        'success': True,
        'data': formats
    })