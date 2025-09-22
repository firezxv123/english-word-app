#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
检查GitHub连接状态的脚本
"""

import subprocess
import os

def run_git_command(command):
    """执行Git命令并返回结果"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd='d:/qodercode'
        )
        return {
            'success': result.returncode == 0,
            'stdout': result.stdout.strip(),
            'stderr': result.stderr.strip(),
            'returncode': result.returncode
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def check_github_connection():
    """检查GitHub连接状态"""
    print("🔍 检查GitHub连接状态")
    print("=" * 40)
    
    # 1. 检查远程仓库配置
    print("\n1️⃣ 检查远程仓库配置...")
    remote_result = run_git_command("git remote -v")
    if remote_result['success']:
        if remote_result['stdout']:
            print("✅ 远程仓库已配置:")
            for line in remote_result['stdout'].split('\n'):
                if line.strip():
                    print(f"   {line}")
        else:
            print("❌ 没有配置远程仓库")
            return False
    else:
        print(f"❌ 检查远程仓库失败: {remote_result.get('stderr', '未知错误')}")
        return False
    
    # 2. 检查Git状态
    print("\n2️⃣ 检查Git状态...")
    status_result = run_git_command("git status --porcelain")
    if status_result['success']:
        if status_result['stdout']:
            changes = status_result['stdout'].split('\n')
            print(f"⚠️  有 {len(changes)} 个文件待提交:")
            for change in changes[:5]:  # 只显示前5个
                if change.strip():
                    print(f"   {change}")
            if len(changes) > 5:
                print(f"   ... 还有 {len(changes) - 5} 个文件")
        else:
            print("✅ 工作目录干净，没有待提交的更改")
    else:
        print(f"❌ 检查状态失败: {status_result.get('stderr', '未知错误')}")
    
    # 3. 检查分支信息
    print("\n3️⃣ 检查分支信息...")
    branch_result = run_git_command("git branch -vv")
    if branch_result['success']:
        print("📋 分支状态:")
        for line in branch_result['stdout'].split('\n'):
            if line.strip():
                print(f"   {line}")
    else:
        print(f"❌ 检查分支失败: {branch_result.get('stderr', '未知错误')}")
    
    # 4. 测试连接到GitHub
    print("\n4️⃣ 测试GitHub连接...")
    
    # 获取远程仓库URL
    remote_url = None
    if remote_result['success'] and remote_result['stdout']:
        for line in remote_result['stdout'].split('\n'):
            if 'github.com' in line and '(fetch)' in line:
                parts = line.split()
                if len(parts) >= 2:
                    remote_url = parts[1]
                    break
    
    if remote_url:
        print(f"🔗 远程仓库URL: {remote_url}")
        
        # 尝试获取远程信息
        fetch_result = run_git_command("git ls-remote --heads origin")
        if fetch_result['success']:
            print("✅ 成功连接到GitHub仓库")
            if fetch_result['stdout']:
                print("📂 远程分支:")
                for line in fetch_result['stdout'].split('\n'):
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 2:
                            branch = parts[1].replace('refs/heads/', '')
                            print(f"   {branch}")
        else:
            print(f"❌ 无法连接到GitHub: {fetch_result.get('stderr', '连接失败')}")
            return False
    else:
        print("❌ 未找到GitHub远程仓库配置")
        return False
    
    # 5. 检查最新提交
    print("\n5️⃣ 最新提交记录...")
    log_result = run_git_command("git log --oneline -n 3")
    if log_result['success']:
        print("📝 最近3次提交:")
        for line in log_result['stdout'].split('\n'):
            if line.strip():
                print(f"   {line}")
    
    print("\n🎉 GitHub连接检查完成!")
    return True

def provide_connection_guide():
    """提供连接指南"""
    print("\n" + "=" * 50)
    print("📚 GitHub连接设置指南")
    print("=" * 50)
    
    print("\n如果还没有连接到GitHub，请按以下步骤操作:")
    print("\n1️⃣ 在GitHub创建新仓库:")
    print("   - 访问 https://github.com")
    print("   - 点击 New repository")
    print("   - 仓库名: english-word-app")
    print("   - 不勾选 Add README")
    
    print("\n2️⃣ 连接本地仓库到GitHub:")
    print("   git remote add origin https://github.com/您的用户名/english-word-app.git")
    print("   git branch -M main")
    print("   git push -u origin main")
    
    print("\n3️⃣ 如果已经有配置但连接失败:")
    print("   - 检查GitHub用户名和密码")
    print("   - 考虑使用Personal Access Token")
    print("   - 检查网络连接")

if __name__ == "__main__":
    success = check_github_connection()
    if not success:
        provide_connection_guide()