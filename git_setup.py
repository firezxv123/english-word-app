import subprocess
import os
import sys

def run_cmd(cmd, cwd=None, ignore_errors=False):
    """运行命令并返回结果"""
    try:
        print(f"执行命令: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
        print(f"返回码: {result.returncode}")
        if result.stdout:
            print(f"输出: {result.stdout}")
        if result.stderr and (result.returncode != 0 or not ignore_errors):
            print(f"错误: {result.stderr}")
        print("-" * 50)
        return result.returncode == 0 or ignore_errors
    except Exception as e:
        print(f"执行失败: {e}")
        return False

def main():
    # 设置工作目录
    work_dir = r'd:\qodercode'
    print(f"工作目录: {work_dir}")
    
    # 1. 检查Git状态
    print("1. 检查Git状态...")
    run_cmd("git status", work_dir, ignore_errors=True)
    
    # 2. 设置用户信息
    print("2. 设置用户信息...")
    if not run_cmd('git config user.email "16352953@qq.com"', work_dir):
        return
    if not run_cmd('git config user.name "firezxv123"', work_dir):
        return
    
    # 3. 添加所有文件
    print("3. 添加所有文件...")
    if not run_cmd("git add .", work_dir):
        return
    
    # 4. 提交更改
    print("4. 提交更改...")
    if not run_cmd('git commit -m "Initial commit: English word learning and testing management system"', work_dir):
        # 如果没有更改需要提交，继续执行
        pass
    
    # 5. 设置远程仓库
    print("5. 设置远程仓库...")
    run_cmd("git remote remove origin", work_dir, ignore_errors=True)
    if not run_cmd("git remote add origin https://github.com/firezxv123/english-word-app.git", work_dir):
        return
    
    # 6. 推送到远程仓库
    print("6. 推送到远程仓库...")
    # 先尝试推送（可能会失败，因为需要认证）
    run_cmd("git push -u origin main", work_dir, ignore_errors=True)
    
    print("Git操作完成!")

if __name__ == "__main__":
    main()