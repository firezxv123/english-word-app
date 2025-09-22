#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Git同步脚本：将代码更改提交到版本库
"""

import subprocess
import os
import sys

def run_command(command, description):
    """执行命令并显示结果"""
    print(f"\n📋 {description}")
    print(f"🔧 执行命令: {command}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd='d:/qodercode'
        )
        
        if result.stdout:
            print(f"✅ 输出:\n{result.stdout}")
        
        if result.stderr:
            print(f"⚠️  错误信息:\n{result.stderr}")
            
        if result.returncode != 0:
            print(f"❌ 命令执行失败，返回码: {result.returncode}")
            return False
        else:
            print(f"✅ 命令执行成功")
            return True
            
    except Exception as e:
        print(f"❌ 执行命令时出错: {str(e)}")
        return False

def main():
    """主函数"""
    print("🎯 Git代码同步程序")
    print("=" * 50)
    
    # 检查是否在正确的目录
    if not os.path.exists('d:/qodercode/.git'):
        print("❌ 错误：不是Git仓库目录")
        return
    
    # 1. 检查Git状态
    if not run_command("git status --porcelain", "检查Git状态"):
        return
    
    # 2. 添加所有文件
    if not run_command("git add .", "添加所有更改的文件"):
        return
    
    # 3. 检查暂存区
    if not run_command("git status --cached", "检查暂存区文件"):
        return
    
    # 4. 提交更改
    commit_message = """完善六年级词库，添加完整的人教版PEP词汇

- 新增 grade6_words_complete.json：包含154个完整的六年级核心词汇
- 新增 grade6_words_additional.json：补充76个额外词汇  
- 新增 grade6_words_extended.json：扩展47个词汇
- 新增专门的六年级词库导入路由 /admin/words/import_grade6
- 更新词库管理界面，添加六年级词库补充按钮
- 解决用户反馈的'6年级词库还缺少很多'问题
- 词库来源：2024年最新人教版PEP小学英语六年级教材
- 涵盖主题：交通方式、地点方位、计划安排、爱好活动、职业工作、情感态度
- 总计：从原来70个词汇增加到200+个词汇"""
    
    commit_command = f'git commit -m "{commit_message}"'
    if not run_command(commit_command, "提交更改"):
        return
    
    # 5. 推送到远程仓库
    if not run_command("git push origin main", "推送到远程仓库"):
        # 如果main分支不存在，尝试master分支
        if not run_command("git push origin master", "推送到远程仓库(master分支)"):
            print("⚠️  推送失败，请检查远程仓库配置")
            return
    
    # 6. 显示最新提交
    run_command("git log --oneline -n 3", "显示最近3次提交")
    
    print("\n🎉 Git同步完成！")
    print("📊 本次更新内容：")
    print("   • 完善了六年级英语词库")
    print("   • 新增了词库管理功能")
    print("   • 提升了用户体验")
    print("   • 解决了词库不完整的问题")

if __name__ == "__main__":
    main()