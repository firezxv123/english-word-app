@echo off
cd /d d:\qodercode
echo Initializing Git repository...
rmdir /s /q .git
git init
git config user.email "16352953@qq.com"
git config user.name "firezxv123"
git add .
git commit -m "Initial commit: English word learning and testing management system"
git remote add origin https://github.com/firezxv123/english-word-app.git
echo Git repository initialized successfully!
pause