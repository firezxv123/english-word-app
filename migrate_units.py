#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据库迁移脚本：调整词库数据以符合2024年新版人教版PEP教材标准
- 3-6年级每个年级分为上下册，共12个单元（六年级下册除外，为10个单元）
- 上册：1-6单元，下册：7-12单元（六年级下册为7-10单元）
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.word import Word
from app.utils.constants import GRADE_UNITS, get_grade_all_units
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_and_fix_word_units():
    """验证和修复词库单元数据"""
    app = create_app()
    
    with app.app_context():
        logger.info("开始验证和修复词库单元数据...")
        
        # 统计信息
        total_words = 0
        fixed_words = 0
        invalid_words = []
        
        # 按年级处理
        for grade in [3, 4, 5, 6]:
            logger.info(f"处理{grade}年级词库数据...")
            
            # 获取该年级的所有单词
            words = Word.query.filter_by(grade=grade).all()
            grade_total = len(words)
            logger.info(f"{grade}年级共有{grade_total}个单词")
            
            # 获取该年级有效的单元范围
            valid_units = get_grade_all_units(grade)
            max_unit = max(valid_units) if valid_units else 12
            
            logger.info(f"{grade}年级有效单元范围: {valid_units}")
            
            for word in words:
                total_words += 1
                
                # 检查单元是否超出范围
                if word.unit > max_unit:
                    logger.warning(f"发现超出范围的单词: {word.word} (年级:{word.grade}, 单元:{word.unit})")
                    
                    # 将超出范围的单元调整到最大单元
                    original_unit = word.unit
                    word.unit = max_unit
                    fixed_words += 1
                    
                    logger.info(f"已修复: {word.word} 单元 {original_unit} -> {word.unit}")
                
                # 检查单元是否为0或负数
                elif word.unit <= 0:
                    logger.warning(f"发现无效单元的单词: {word.word} (年级:{word.grade}, 单元:{word.unit})")
                    
                    # 将无效单元设置为1
                    original_unit = word.unit
                    word.unit = 1
                    fixed_words += 1
                    
                    logger.info(f"已修复: {word.word} 单元 {original_unit} -> {word.unit}")
        
        # 提交更改
        if fixed_words > 0:
            try:
                db.session.commit()
                logger.info(f"成功修复了{fixed_words}个单词的单元数据")
            except Exception as e:
                db.session.rollback()
                logger.error(f"提交修复失败: {str(e)}")
                return False
        
        logger.info(f"词库数据验证完成:")
        logger.info(f"- 总词汇数: {total_words}")
        logger.info(f"- 修复词汇数: {fixed_words}")
        
        return True

def check_unit_distribution():
    """检查各年级单元分布情况"""
    app = create_app()
    
    with app.app_context():
        logger.info("检查各年级单元分布情况...")
        
        for grade in [3, 4, 5, 6]:
            logger.info(f"\n{grade}年级单元分布:")
            
            # 统计每个单元的单词数
            from sqlalchemy import func
            unit_stats = db.session.query(
                Word.unit,
                func.count(Word.id).label('count')
            ).filter_by(grade=grade).group_by(Word.unit).order_by(Word.unit).all()
            
            total_words = sum(stat.count for stat in unit_stats)
            
            for unit, count in unit_stats:
                semester = "上册" if unit <= 6 else "下册"
                logger.info(f"  第{unit}单元({semester}): {count}个单词")
            
            logger.info(f"  {grade}年级总词汇: {total_words}个")
            
            # 检查是否符合标准
            valid_units = get_grade_all_units(grade)
            expected_units = len(valid_units)
            actual_units = len(unit_stats)
            
            if actual_units <= expected_units:
                logger.info(f"  ✓ 单元数量正常 (实际:{actual_units}, 预期:≤{expected_units})")
            else:
                logger.warning(f"  ⚠ 单元数量超出预期 (实际:{actual_units}, 预期:≤{expected_units})")

def generate_unit_report():
    """生成单元分布报告"""
    app = create_app()
    
    with app.app_context():
        logger.info("生成单元分布报告...")
        
        report_lines = []
        report_lines.append("# 词库单元分布报告")
        report_lines.append(f"报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        for grade in [3, 4, 5, 6]:
            report_lines.append(f"## {grade}年级")
            
            from sqlalchemy import func
            unit_stats = db.session.query(
                Word.unit,
                func.count(Word.id).label('count')
            ).filter_by(grade=grade).group_by(Word.unit).order_by(Word.unit).all()
            
            total_words = sum(stat.count for stat in unit_stats)
            
            report_lines.append(f"总词汇数: {total_words}")
            report_lines.append("")
            report_lines.append("| 单元 | 学期 | 词汇数 |")
            report_lines.append("|------|------|--------|")
            
            for unit, count in unit_stats:
                semester = "上册" if unit <= 6 else "下册"
                report_lines.append(f"| {unit} | {semester} | {count} |")
            
            report_lines.append("")
        
        # 写入报告文件
        report_path = "docs/unit_distribution_report.md"
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        
        logger.info(f"报告已生成: {report_path}")

if __name__ == '__main__':
    import argparse
    from datetime import datetime
    
    parser = argparse.ArgumentParser(description='词库数据迁移工具')
    parser.add_argument('--fix', action='store_true', help='修复无效的单元数据')
    parser.add_argument('--check', action='store_true', help='检查单元分布情况')
    parser.add_argument('--report', action='store_true', help='生成单元分布报告')
    
    args = parser.parse_args()
    
    if args.fix:
        validate_and_fix_word_units()
    
    if args.check:
        check_unit_distribution()
    
    if args.report:
        generate_unit_report()
    
    if not any([args.fix, args.check, args.report]):
        print("请指定操作参数:")
        print("  --fix   : 修复无效的单元数据")
        print("  --check : 检查单元分布情况")
        print("  --report: 生成单元分布报告")
        print("\n示例:")
        print("  python migrate_units.py --fix --check")
        print("  python migrate_units.py --report")