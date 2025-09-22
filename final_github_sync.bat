@echo off
chcp 65001 >nul
cd /d "d:\qodercode"

echo.
echo ========================================
echo    🚀 GitHub 最终同步程序
echo ========================================
echo.

echo 📂 当前目录: %CD%
echo.

echo 1️⃣ 检查Git配置状态...
echo 📋 远程仓库配置:
git remote -v
echo.

echo 📋 当前分支状态:
git branch -vv
echo.

echo 2️⃣ 检查待提交的文件...
git status --short
echo.

echo 3️⃣ 添加所有新文件和更改...
git add .
echo ✅ 文件已添加到暂存区
echo.

echo 4️⃣ 提交更改...
git commit -m "完善六年级词库，添加GitHub同步功能

- 新增完整的六年级词库文件
- 修复GitHub远程仓库配置
- 添加词库管理和同步脚本
- 解决用户反馈的词库不完整问题
- 词库来源：2024年人教版PEP教材"

echo.

echo 5️⃣ 推送到GitHub...
echo 📤 正在推送到 origin/main...
git push -u origin main

if errorlevel 1 (
    echo.
    echo ⚠️  推送失败，可能的原因：
    echo    1. 需要GitHub身份验证
    echo    2. 网络连接问题  
    echo    3. 仓库权限问题
    echo.
    echo 💡 解决建议：
    echo    - 检查GitHub用户名和密码
    echo    - 使用Personal Access Token代替密码
    echo    - 确保仓库存在: https://github.com/firezxv123/english-word-app
    echo.
    echo 🔧 手动推送命令：
    echo    git push -u origin main
) else (
    echo.
    echo 🎉 成功推送到GitHub！
    echo 🔗 查看项目: https://github.com/firezxv123/english-word-app
    echo ✅ GitHub连接已成功建立
)

echo.
echo 6️⃣ 显示最新状态...
echo 📝 最近的提交:
git log --oneline -n 3

echo 📊 当前状态:
git status

echo.
echo ========================================
echo    同步操作完成！
echo ========================================
echo.
echo 📋 配置总结:
echo    • 远程仓库: origin
echo    • 仓库URL: https://github.com/firezxv123/english-word-app.git  
echo    • 本地分支: main
echo    • Git用户: Developer ^<dev@example.com^>
echo.

pause