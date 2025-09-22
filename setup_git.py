import subprocess
import os
import shutil

def run_cmd(cmd, cwd=None):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
        print(f"命令: {cmd}")
        print(f"返回码: {result.returncode}")
        if result.stdout:
            print(f"输出: {result.stdout}")
        if result.stderr:
            print(f"错误: {result.stderr}")
        print("-" * 50)
        return result.returncode == 0
    except Exception as e:
        print(f"执行失败: {e}")
        return False

def main():
    # 设置工作目录
    work_dir = r'd:\qodercode'
    print(f"工作目录: {work_dir}")
    
    # 1. 删除现有的.git目录
    git_dir = os.path.join(work_dir, '.git')
    if os.path.exists(git_dir):
        print("删除现有的.git目录...")
        try:
            shutil.rmtree(git_dir)
            print("成功删除.git目录")
        except Exception as e:
            print(f"删除.git目录失败: {e}")
            return
    
    # 2. 初始化Git仓库
    print("初始化Git仓库...")
    if not run_cmd("git init", work_dir):
        return
    
    # 3. 设置用户信息
    print("设置用户信息...")
    if not run_cmd('git config user.email "16352953@qq.com"', work_dir):
        return
    if not run_cmd('git config user.name "firezxv123"', work_dir):
        return
    
    # 4. 添加所有文件
    print("添加所有文件...")
    if not run_cmd("git add .", work_dir):
        return
    
    # 5. 提交
    print("提交更改...")
    if not run_cmd('git commit -m "Initial commit: English word learning and testing management system"', work_dir):
        return
    
    # 6. 添加远程仓库
    print("添加远程仓库...")
    if not run_cmd("git remote add origin https://github.com/firezxv123/english-word-app.git", work_dir):
        return
    
    print("Git仓库初始化完成!")

if __name__ == "__main__":
    main()