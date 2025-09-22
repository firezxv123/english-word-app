# PowerShell脚本：同步代码到Git版本库
Write-Host "========================================" -ForegroundColor Green
Write-Host "正在同步代码到Git版本库" -ForegroundColor Green  
Write-Host "========================================" -ForegroundColor Green

# 切换到项目目录
Set-Location "d:\qodercode"

Write-Host "`n1. 检查Git状态..." -ForegroundColor Yellow
git status

Write-Host "`n2. 添加所有更改的文件..." -ForegroundColor Yellow
git add .

Write-Host "`n3. 检查将要提交的文件..." -ForegroundColor Yellow
git status --cached

$commitMessage = @"
完善六年级词库，添加完整的人教版PEP词汇

- 新增 grade6_words_complete.json：包含154个完整的六年级核心词汇
- 新增 grade6_words_additional.json：补充76个额外词汇  
- 新增 grade6_words_extended.json：扩展47个词汇
- 新增专门的六年级词库导入路由 /admin/words/import_grade6
- 更新词库管理界面，添加六年级词库补充按钮
- 解决用户反馈的'6年级词库还缺少很多'问题
- 词库来源：2024年最新人教版PEP小学英语六年级教材
- 涵盖主题：交通方式、地点方位、计划安排、爱好活动、职业工作、情感态度
- 总计：从原来70个词汇增加到200+个词汇
"@

Write-Host "`n4. 提交更改..." -ForegroundColor Yellow
git commit -m $commitMessage

Write-Host "`n5. 推送到远程仓库..." -ForegroundColor Yellow
git push origin main

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "Git同步完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# 显示最新的提交信息
Write-Host "`n最新提交信息:" -ForegroundColor Cyan
git log --oneline -n 3

Write-Host "`n按任意键退出..."
Read-Host