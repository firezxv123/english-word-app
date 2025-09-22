import subprocess
import os

# 切换到项目目录
os.chdir('d:/qodercode')

print("🎯 开始Git同步...")

# 执行Git命令
try:
    # 1. 添加所有文件
    print("1️⃣ 添加文件...")
    result1 = subprocess.run(['git', 'add', '.'], capture_output=True, text=True)
    print(f"✅ git add 完成: {result1.returncode}")
    
    # 2. 提交更改
    print("2️⃣ 提交更改...")
    commit_msg = "完善六年级词库：新增完整的人教版PEP词汇，解决词库不完整问题"
    result2 = subprocess.run(['git', 'commit', '-m', commit_msg], capture_output=True, text=True)
    print(f"✅ git commit 完成: {result2.returncode}")
    if result2.stdout:
        print(f"输出: {result2.stdout}")
    if result2.stderr:
        print(f"信息: {result2.stderr}")
    
    # 3. 推送到远程
    print("3️⃣ 推送到远程...")
    result3 = subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True, text=True)
    print(f"✅ git push 完成: {result3.returncode}")
    if result3.stdout:
        print(f"输出: {result3.stdout}")
    if result3.stderr:
        print(f"信息: {result3.stderr}")
    
    # 如果main失败，尝试master
    if result3.returncode != 0:
        print("📝 尝试推送到master分支...")
        result4 = subprocess.run(['git', 'push', 'origin', 'master'], capture_output=True, text=True)
        print(f"✅ git push master 完成: {result4.returncode}")
        if result4.stdout:
            print(f"输出: {result4.stdout}")
        if result4.stderr:
            print(f"信息: {result4.stderr}")
    
    print("🎉 Git同步完成!")
    
except Exception as e:
    print(f"❌ 出错: {str(e)}")