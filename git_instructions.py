import os
import shutil

# 删除现有的.git目录
git_dir = r'd:\qodercode\.git'
if os.path.exists(git_dir):
    print("删除现有的.git目录...")
    try:
        shutil.rmtree(git_dir)
        print("成功删除.git目录")
    except Exception as e:
        print(f"删除.git目录失败: {e}")

print("请手动执行以下命令:")
print("1. cd /d d:\\qodercode")
print("2. git init")
print("3. git config user.email \"16352953@qq.com\"")
print("4. git config user.name \"firezxv123\"")
print("5. git add .")
print("6. git commit -m \"Initial commit: English word learning and testing management system\"")
print("7. git remote add origin https://github.com/firezxv123/english-word-app.git")
print("8. git push -u origin main")