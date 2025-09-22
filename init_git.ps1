Set-Location -Path "d:\qodercode"
Write-Host "Initializing Git repository..."
Remove-Item -Path ".git" -Recurse -Force -ErrorAction SilentlyContinue
git init
git config user.email "16352953@qq.com"
git config user.name "firezxv123"
git add .
git commit -m "Initial commit: English word learning and testing management system"
git remote add origin https://github.com/firezxv123/english-word-app.git
Write-Host "Git repository initialized successfully!"