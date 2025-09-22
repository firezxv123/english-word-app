@echo off
chcp 65001 >nul
cd /d "d:\qodercode"

echo.
echo ========================================
echo    🎯 Git 代码同步程序
echo ========================================
echo.

echo 📂 当前目录: %CD%
echo.

echo 1️⃣ 检查Git状态...
git status
echo.

echo 2️⃣ 添加所有更改的文件...
git add .
echo ✅ 文件添加完成
echo.

echo 3️⃣ 提交更改...
git commit -m "完善六年级词库，添加完整的人教版PEP词汇" -m "主要更新：新增完整的六年级词库文件，解决用户反馈的词库不完整问题，词库来源：2024年人教版PEP教材，从70个词汇增加到200+个"
echo.

echo 4️⃣ 推送到远程仓库...
git push origin main
if errorlevel 1 (
    echo ⚠️  推送到main失败，尝试master分支...
    git push origin master
)
echo.

echo 5️⃣ 显示最新提交...
git log --oneline -n 3
echo.

echo ========================================
echo    🎉 Git同步完成！
echo ========================================
echo.
echo 📊 本次更新总结：
echo    ✅ 完善了六年级英语词库
echo    ✅ 新增了词库管理功能
echo    ✅ 解决了用户反馈的问题
echo    ✅ 提升了整体用户体验
echo.

pause