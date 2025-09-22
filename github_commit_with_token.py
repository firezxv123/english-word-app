#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
使用GitHub Token进行代码提交的脚本
"""

import subprocess
import os

def run_git_command(cmd, description, check_error=True):
    """执行Git命令"""
    print(f"\n🔧 {description}")
    print(f"执行命令: {cmd}")
    
    try:
        # 设置环境变量，包含GitHub Token
        env = os.environ.copy()
        env['GIT_ASKPASS'] = 'echo'
        env['GIT_USERNAME'] = 'firezxv123'
        env['GIT_PASSWORD'] = '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'
        
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            cwd='d:/qodercode',
            env=env
        )
        
        print(f"返回码: {result.returncode}")
        
        if result.stdout:
            print(f"✅ 输出:\n{result.stdout}")
        
        if result.stderr:
            if result.returncode == 0:
                print(f"ℹ️  信息:\n{result.stderr}")
            else:
                print(f"❌ 错误:\n{result.stderr}")
        
        if check_error and result.returncode != 0:
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 执行失败: {e}")
        return False

def main():
    print("🚀 GitHub Token 提交程序")
    print("=" * 50)
    print(f"📋 GitHub用户名: firezxv123")
    print(f"🔑 使用Personal Access Token认证")
    print("=" * 50)
    
    # 1. 检查当前状态
    print("\n1️⃣ 检查当前Git状态...")
    run_git_command("git status", "检查工作区状态", False)
    
    # 2. 检查远程配置
    print("\n2️⃣ 检查远程仓库配置...")
    run_git_command("git remote -v", "查看远程仓库", False)
    
    # 3. 添加所有文件
    print("\n3️⃣ 添加所有更改的文件...")
    if run_git_command("git add .", "添加文件到暂存区"):
        print("✅ 文件添加成功")
    else:
        print("❌ 文件添加失败")
        return
    
    # 4. 提交更改
    print("\n4️⃣ 提交更改...")
    commit_message = """完善六年级词库，添加GitHub同步功能

📚 主要更新内容：
- 新增完整的六年级词库文件 (grade6_words_complete.json)
- 新增词库补充文件 (grade6_words_additional.json, grade6_words_extended.json)
- 添加词库管理界面和导入功能
- 修复GitHub远程仓库配置
- 解决用户反馈的'6年级词库还缺少很多'问题

🎯 技术改进：
- 词库来源：2024年人教版PEP教材
- 词汇数量：从70个增加到200+个
- 添加GitHub同步脚本和验证工具
- 完善Web管理界面

🔧 配置优化：
- 修复远程仓库名称为标准的origin
- 添加Token认证支持
- 完善Git工作流程"""
    
    if run_git_command(f'git commit -m "{commit_message}"', "提交代码", False):
        print("✅ 提交成功")
    else:
        print("ℹ️  可能没有新的更改需要提交")
    
    # 5. 使用Token推送到GitHub
    print("\n5️⃣ 推送到GitHub（使用Token认证）...")
    
    # 修改远程URL以包含Token认证
    remote_url_with_token = "https://firezxv123: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@github.com/firezxv123/english-word-app.git"
    
    # 临时设置远程URL
    run_git_command(f'git remote set-url origin "{remote_url_with_token}"', "设置Token认证URL", False)
    
    # 推送到GitHub
    success = run_git_command("git push -u origin main", "推送到GitHub")
    
    # 恢复原始URL（安全起见）
    run_git_command('git remote set-url origin "https://github.com/firezxv123/english-word-app.git"', "恢复原始URL", False)
    
    if success:
        print("\n🎉 成功推送到GitHub！")
        print("🔗 查看项目: https://github.com/firezxv123/english-word-app")
        print("✅ 您的小学英语单词复习应用已同步到GitHub")
        
        # 6. 显示最新状态
        print("\n6️⃣ 显示最新状态...")
        run_git_command("git log --oneline -n 3", "最近的提交记录", False)
        run_git_command("git status", "最终状态", False)
        
    else:
        print("\n❌ 推送失败")
        print("💡 可能的问题：")
        print("   1. Token已过期或无效")
        print("   2. 仓库不存在或无权限")
        print("   3. 网络连接问题")
        print("   4. 分支保护规则限制")

if __name__ == "__main__":
    main()