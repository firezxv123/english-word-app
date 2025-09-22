#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import io
import json
from datetime import datetime
from flask import current_app
import os
import logging

logger = logging.getLogger(__name__)

# 尝试导入reportlab，如果没有安装则使用简化版本
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    logger.warning('未reportlab安装，PDF功能不可用')

class ExportService:
    """数据导出服务"""
    
    @staticmethod
    def export_words_to_csv(words, include_headers=True):
        """导出单词到CSV格式"""
        try:
            output = io.StringIO()
            writer = csv.writer(output, quoting=csv.QUOTE_ALL)
            
            if include_headers:
                headers = [
                    '单词', '中文含义', '音标', '拼读拆分', '记忆方法',
                    '年级', '单元', '教材版本', '音频链接', '创建时间'
                ]
                writer.writerow(headers)
            
            for word in words:
                row = [
                    word.word,
                    word.chinese_meaning,
                    word.phonetic or '',
                    word.phonics_breakdown or '',
                    word.memory_method or '',
                    word.grade,
                    word.unit,
                    word.book_version,
                    word.audio_url or '',
                    word.created_at.strftime('%Y-%m-%d %H:%M:%S') if word.created_at else ''
                ]
                writer.writerow(row)
            
            csv_content = output.getvalue()
            output.close()
            
            logger.info(f"成功导出 {len(words)} 个单词到CSV")
            return csv_content, None
            
        except Exception as e:
            error_msg = f"CSV导出失败: {str(e)}"
            logger.error(error_msg)
            return None, error_msg
    
    @staticmethod
    def export_words_to_pdf(words, title="单词列表"):
        """导出单词到PDF格式"""
        if not REPORTLAB_AVAILABLE:
            return None, "PDF功能不可用，请安装reportlab库"
        
        try:
            # 创建内存文件
            buffer = io.BytesIO()
            
            # 创建PDF文档
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=0.5*inch,
                leftMargin=0.5*inch,
                topMargin=0.75*inch,
                bottomMargin=0.5*inch
            )
            
            # 获取样式
            styles = getSampleStyleSheet()
            story = []
            
            # 标题
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                spaceAfter=30,
                alignment=1  # 居中
            )
            story.append(Paragraph(title, title_style))
            
            # 添加生成时间
            time_style = ParagraphStyle(
                'TimeStyle',
                parent=styles['Normal'],
                fontSize=10,
                textColor=colors.grey,
                alignment=1
            )
            story.append(Paragraph(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", time_style))
            story.append(Spacer(1, 20))
            
            # 统计信息
            stats_data = ExportService._get_words_statistics(words)
            stats_table = Table([
                ['统计项目', '数量'],
                ['单词总数', str(len(words))],
                ['涉及年级', ', '.join(map(str, sorted(stats_data['grades'])))],
                ['涉及单元', f"{stats_data['min_unit']} - {stats_data['max_unit']}"],
            ])
            
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(stats_table)
            story.append(Spacer(1, 20))
            
            # 单词表格
            if words:
                # 按年级和单元排序
                sorted_words = sorted(words, key=lambda w: (w.grade, w.unit, w.word))
                
                # 创建表格数据
                table_data = [['单词', '中文含义', '年级', '单元', '拼读', '记忆方法']]
                
                for word in sorted_words:
                    row = [
                        word.word,
                        word.chinese_meaning[:30] + '...' if len(word.chinese_meaning) > 30 else word.chinese_meaning,
                        f"{word.grade}年级",
                        f"第{word.unit}单元",
                        word.phonics_breakdown[:20] + '...' if word.phonics_breakdown and len(word.phonics_breakdown) > 20 else (word.phonics_breakdown or ''),
                        word.memory_method[:30] + '...' if word.memory_method and len(word.memory_method) > 30 else (word.memory_method or '')
                    ]
                    table_data.append(row)
                
                # 创建表格
                table = Table(table_data, colWidths=[1*inch, 1.5*inch, 0.8*inch, 0.8*inch, 1.2*inch, 1.7*inch])
                
                # 设置表格样式
                table.setStyle(TableStyle([
                    # 标题行样式
                    ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    
                    # 数据行样式
                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    
                    # 交替行颜色
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
                ]))
                
                story.append(table)
            
            # 生成PDF
            doc.build(story)
            
            pdf_content = buffer.getvalue()
            buffer.close()
            
            logger.info(f"成功导出 {len(words)} 个单词到PDF")
            return pdf_content, None
            
        except Exception as e:
            error_msg = f"PDF导出失败: {str(e)}"
            logger.error(error_msg)
            return None, error_msg
    
    @staticmethod
    def export_study_report_to_pdf(user, study_data, test_data):
        """导出学习报告到PDF"""
        if not REPORTLAB_AVAILABLE:
            return None, "PDF功能不可用，请安装reportlab库"
        
        try:
            buffer = io.BytesIO()
            
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=0.5*inch,
                leftMargin=0.5*inch,
                topMargin=0.75*inch,
                bottomMargin=0.5*inch
            )
            
            styles = getSampleStyleSheet()
            story = []
            
            # 报告标题
            title_style = ParagraphStyle(
                'ReportTitle',
                parent=styles['Heading1'],
                fontSize=20,
                spaceAfter=30,
                alignment=1
            )
            story.append(Paragraph(f"{user.username} 的学习报告", title_style))
            
            # 用户信息
            user_info_style = ParagraphStyle(
                'UserInfo',
                parent=styles['Normal'],
                fontSize=12,
                spaceAfter=10
            )
            story.append(Paragraph(f"用户名: {user.username}", user_info_style))
            story.append(Paragraph(f"年级: {user.grade}年级", user_info_style))
            story.append(Paragraph(f"报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", user_info_style))
            story.append(Spacer(1, 20))
            
            # 学习统计
            story.append(Paragraph("学习统计", styles['Heading2']))
            
            study_table = Table([
                ['统计项目', '数值'],
                ['总学习单词数', str(study_data.get('total_studied', 0))],
                ['已掌握单词数', str(study_data.get('mastered', 0))],
                ['掌握率', f"{study_data.get('mastery_rate', 0):.1f}%"],
                ['当前单元进度', str(study_data.get('current_unit_studied', 0))],
            ])
            
            study_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(study_table)
            story.append(Spacer(1, 20))
            
            # 测验统计
            if test_data:
                story.append(Paragraph("测验统计", styles['Heading2']))
                
                test_table = Table([
                    ['统计项目', '数值'],
                    ['总测验次数', str(test_data.get('total_tests', 0))],
                    ['平均正确率', f"{test_data.get('average_accuracy', 0):.1f}%"],
                    ['最高正确率', f"{test_data.get('highest_accuracy', 0):.1f}%"],
                    ['最近测验时间', test_data.get('last_test_date', '无')],
                ])
                
                test_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(test_table)
            
            # 生成PDF
            doc.build(story)
            
            pdf_content = buffer.getvalue()
            buffer.close()
            
            logger.info(f"成功生成用户 {user.username} 的学习报告")
            return pdf_content, None
            
        except Exception as e:
            error_msg = f"学习报告生成失败: {str(e)}"
            logger.error(error_msg)
            return None, error_msg
    
    @staticmethod
    def export_to_json(data, formatted=True):
        """导出数据到JSON格式"""
        try:
            if formatted:
                json_content = json.dumps(data, ensure_ascii=False, indent=2)
            else:
                json_content = json.dumps(data, ensure_ascii=False)
            
            return json_content, None
            
        except Exception as e:
            error_msg = f"JSON导出失败: {str(e)}"
            logger.error(error_msg)
            return None, error_msg
    
    @staticmethod
    def _get_words_statistics(words):
        """获取单词统计信息"""
        grades = set()
        units = set()
        
        for word in words:
            grades.add(word.grade)
            units.add(word.unit)
        
        return {
            'grades': list(grades),
            'units': list(units),
            'min_unit': min(units) if units else 0,
            'max_unit': max(units) if units else 0,
            'total_words': len(words)
        }