import subprocess
import os

# 切换到项目目录
os.chdir('d:/qodercode')

print("🔍 验证GitHub连接状态")
print("=" * 30)

# 检查远程配置
try:
    result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
    print(f"✅ 远程仓库配置:")
    if result.stdout:
        for line in result.stdout.strip().split('\n'):
            print(f"   {line}")
    else:
        print("   ❌ 没有配置远程仓库")
except Exception as e:
    print(f"❌ 检查远程配置失败: {e}")

# 检查Git状态
try:
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    if result.stdout.strip():
        print(f"\n📝 待提交的文件:")
        for line in result.stdout.strip().split('\n'):
            print(f"   {line}")
    else:
        print(f"\n✅ 工作目录干净")
except Exception as e:
    print(f"❌ 检查状态失败: {e}")

# 尝试添加文件并提交
print(f"\n🚀 尝试提交和推送...")
try:
    # 添加所有文件
    subprocess.run(['git', 'add', '.'], check=True)
    print("✅ 文件已添加到暂存区")
    
    # 提交
    result = subprocess.run(['git', 'commit', '-m', '完善六年级词库，添加完整的人教版PEP词汇'], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ 提交成功")
    else:
        print(f"⚠️ 提交信息: {result.stdout}")
    
    # 推送
    result = subprocess.run(['git', 'push', '-u', 'origin', 'main'], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print("🎉 成功推送到GitHub!")
        print("🔗 查看项目: https://github.com/firezxv123/english-word-app")
    else:
        print(f"❌ 推送失败:")
        print(f"   错误信息: {result.stderr}")
        print(f"   输出信息: {result.stdout}")
        
except Exception as e:
    print(f"❌ 操作失败: {e}")

print(f"\n📊 最终状态:")
try:
    result = subprocess.run(['git', 'log', '--oneline', '-n', '3'], capture_output=True, text=True)
    if result.stdout:
        print("最近的提交:")
        for line in result.stdout.strip().split('\n'):
            print(f"   {line}")
except:
    print("   无法获取提交历史")