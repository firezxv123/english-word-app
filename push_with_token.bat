@echo off
chcp 65001 >nul
cd /d "d:\qodercode"

echo.
echo ========================================
echo    🚀 使用Token推送到GitHub
echo ========================================
echo.

echo 📂 当前目录: %CD%
echo 👤 GitHub用户: firezxv123
echo 🔑 使用Personal Access Token认证
echo.

echo 1️⃣ 检查Git状态...
git status --short
echo.

echo 2️⃣ 添加所有文件...
git add .
echo ✅ 文件已添加
echo.

echo 3️⃣ 提交更改...
git commit -m "完善六年级词库，添加GitHub同步功能

- 新增完整的六年级词库文件
- 添加GitHub Token认证支持  
- 修复远程仓库配置
- 解决词库不完整问题
- 词库来源：2024年人教版PEP教材"

echo.

echo 4️⃣ 使用Token推送到GitHub...
echo 📤 正在推送...

rem 使用Token进行认证推送
git push https://firezxv123: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@github.com/firezxv123/english-word-app.git main

if errorlevel 1 (
    echo.
    echo ❌ 推送失败
    echo 💡 可能的原因：
    echo    1. Token已过期
    echo    2. 仓库不存在
    echo    3. 网络问题
    echo    4. 权限不足
    echo.
    echo 🔧 请检查：
    echo    - Token是否有效
    echo    - 仓库是否存在: https://github.com/firezxv123/english-word-app
    echo    - 网络连接是否正常
) else (
    echo.
    echo 🎉 推送成功！
    echo 🔗 查看项目: https://github.com/firezxv123/english-word-app
    echo ✅ 代码已成功同步到GitHub
    
    echo.
    echo 📋 最新提交记录:
    git log --oneline -n 3
)

echo.
echo ========================================
echo    操作完成
echo ========================================

pause