@echo off
cd /d d:\qodercode

echo ========================================
echo 正在同步代码到Git版本库
echo ========================================

echo.
echo 1. 检查Git状态...
git status

echo.
echo 2. 添加所有更改的文件...
git add .

echo.
echo 3. 检查将要提交的文件...
git status --cached

echo.
echo 4. 提交更改...
git commit -m "完善六年级词库，添加完整的人教版PEP词汇

- 新增 grade6_words_complete.json：包含154个完整的六年级核心词汇
- 新增 grade6_words_additional.json：补充76个额外词汇  
- 新增 grade6_words_extended.json：扩展47个词汇
- 新增专门的六年级词库导入路由 /admin/words/import_grade6
- 更新词库管理界面，添加六年级词库补充按钮
- 解决用户反馈的'6年级词库还缺少很多'问题
- 词库来源：2024年最新人教版PEP小学英语六年级教材
- 涵盖主题：交通方式、地点方位、计划安排、爱好活动、职业工作、情感态度
- 总计：从原来70个词汇增加到200+个词汇"

echo.
echo 5. 推送到远程仓库...
git push origin main

echo.
echo ========================================
echo Git同步完成！
echo ========================================
pause