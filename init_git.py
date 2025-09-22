import subprocess
import os

# 设置工作目录
os.chdir(r'd:\qodercode')

def run_command(cmd):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(f"命令: {cmd}")
        print(f"返回码: {result.returncode}")
        if result.stdout:
            print(f"输出: {result.stdout}")
        if result.stderr:
            print(f"错误: {result.stderr}")
        return result
    except Exception as e:
        print(f"执行失败: {e}")
        return None

print("开始初始化Git仓库...")

# 删除现有的.git目录
print("删除现有的.git目录...")
run_command("rmdir /s /q .git")

# 初始化Git仓库
print("初始化Git仓库...")
run_command("git init")

# 设置用户信息
print("设置用户信息...")
run_command('git config user.email "16352953@qq.com"')
run_command('git config user.name "firezxv123"')

# 添加所有文件
print("添加所有文件...")
run_command("git add .")

# 提交
print("提交更改...")
run_command('git commit -m "Initial commit: English word learning and testing management system"')

# 添加远程仓库
print("添加远程仓库...")
run_command("git remote add origin https://github.com/firezxv123/english-word-app.git")

print("Git初始化完成!")