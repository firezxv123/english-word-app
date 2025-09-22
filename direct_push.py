import subprocess
import os

print("🚀 直接使用Token推送到GitHub")
print("=" * 40)

# 切换到项目目录
os.chdir('d:/qodercode')

try:
    # 1. 添加所有文件
    print("1️⃣ 添加文件...")
    result1 = subprocess.run(['git', 'add', '.'], capture_output=True, text=True)
    print(f"✅ git add 返回码: {result1.returncode}")
    
    # 2. 提交更改
    print("2️⃣ 提交更改...")
    result2 = subprocess.run([
        'git', 'commit', '-m', 
        '完善六年级词库，添加GitHub同步功能\n\n- 新增完整的六年级词库文件\n- 添加GitHub Token认证支持\n- 解决词库不完整问题'
    ], capture_output=True, text=True)
    print(f"✅ git commit 返回码: {result2.returncode}")
    if result2.stdout:
        print(f"提交输出: {result2.stdout}")
    if result2.stderr:
        print(f"提交信息: {result2.stderr}")
    
    # 3. 使用Token推送
    print("3️⃣ 推送到GitHub...")
    token_url = "https://firezxv123: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@github.com/firezxv123/english-word-app.git"
    
    result3 = subprocess.run([
        'git', 'push', token_url, 'main'
    ], capture_output=True, text=True)
    
    print(f"推送返回码: {result3.returncode}")
    
    if result3.returncode == 0:
        print("🎉 推送成功！")
        print("🔗 查看项目: https://github.com/firezxv123/english-word-app")
        
        if result3.stdout:
            print(f"推送输出: {result3.stdout}")
        if result3.stderr:
            print(f"推送信息: {result3.stderr}")
            
        # 显示最新提交
        print("\n📋 最新提交:")
        log_result = subprocess.run(['git', 'log', '--oneline', '-n', '3'], 
                                  capture_output=True, text=True)
        if log_result.stdout:
            print(log_result.stdout)
            
    else:
        print("❌ 推送失败")
        print(f"错误输出: {result3.stderr}")
        print(f"标准输出: {result3.stdout}")
        
        print("\n💡 可能的解决方案:")
        print("1. 检查Token是否有效")
        print("2. 确认仓库存在")
        print("3. 检查网络连接")
    
except Exception as e:
    print(f"❌ 执行出错: {e}")

print("\n🏁 操作完成")