@echo off
chcp 65001 >nul
cd /d "d:\qodercode"

echo.
echo ========================================
echo    🔧 修复GitHub连接配置
echo ========================================
echo.

echo 📂 当前目录: %CD%
echo.

echo 1️⃣ 检查当前远程仓库配置...
git remote -v
echo.

echo 2️⃣ 修复远程仓库配置...
echo 📝 移除旧的远程仓库配置...
git remote remove english-word-app 2>nul

echo 📝 添加标准的origin远程仓库...
git remote add origin https://github.com/firezxv123/english-word-app.git

echo ✅ 远程仓库配置已修复
echo.

echo 3️⃣ 验证新的配置...
git remote -v
echo.

echo 4️⃣ 设置上游分支并推送...
echo 📤 推送到GitHub（首次推送可能需要身份验证）...
git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo ⚠️  推送失败，可能的原因：
    echo    1. 需要GitHub身份验证（用户名/密码或Token）
    echo    2. 网络连接问题
    echo    3. 仓库不存在或无权限
    echo.
    echo 💡 建议：
    echo    - 确保GitHub仓库存在: https://github.com/firezxv123/english-word-app
    echo    - 检查用户名和密码
    echo    - 考虑使用Personal Access Token
) else (
    echo ✅ 成功推送到GitHub!
    echo.
    echo 🎉 GitHub连接已成功建立！
    echo 🔗 查看您的项目: https://github.com/firezxv123/english-word-app
)

echo.
echo 5️⃣ 最终状态检查...
git status
echo.

echo ========================================
echo    修复完成！
echo ========================================

pause