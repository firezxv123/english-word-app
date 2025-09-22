#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import os

def run_command(cmd, description):
    """执行命令并显示结果"""
    print(f"\n🔧 {description}")
    print(f"执行: {cmd}")
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            cwd='d:/qodercode'
        )
        
        print(f"返回码: {result.returncode}")
        if result.stdout:
            print(f"输出:\n{result.stdout}")
        if result.stderr:
            print(f"错误:\n{result.stderr}")
        
        return result.returncode == 0
    except Exception as e:
        print(f"执行失败: {e}")
        return False

def main():
    print("🚀 修复GitHub连接")
    print("=" * 40)
    
    # 1. 检查当前远程配置
    run_command("git remote -v", "检查当前远程配置")
    
    # 2. 移除旧配置
    run_command("git remote remove english-word-app", "移除旧的远程配置")
    
    # 3. 添加标准配置
    run_command("git remote add origin https://github.com/firezxv123/english-word-app.git", "添加标准远程配置")
    
    # 4. 验证新配置
    run_command("git remote -v", "验证新配置")
    
    # 5. 检查状态
    run_command("git status", "检查Git状态")
    
    # 6. 添加所有文件
    run_command("git add .", "添加所有文件")
    
    # 7. 提交更改
    run_command('git commit -m "完善六年级词库，添加完整的人教版PEP词汇"', "提交更改")
    
    # 8. 推送到GitHub
    print("\n🚀 推送到GitHub...")
    success = run_command("git push -u origin main", "推送到GitHub")
    
    if success:
        print("\n✅ GitHub连接修复成功！")
        print("🔗 查看项目: https://github.com/firezxv123/english-word-app")
    else:
        print("\n⚠️ 推送失败，可能需要身份验证")
        print("💡 请检查：")
        print("  1. GitHub用户名和密码")
        print("  2. 网络连接")
        print("  3. 仓库权限")

if __name__ == "__main__":
    main()