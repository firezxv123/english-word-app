# PowerShell脚本：推送代码到GitHub
# 使用Token认证

Write-Host "🚀 开始推送代码到GitHub" -ForegroundColor Green
Write-Host "用户名: firezxv123" -ForegroundColor Yellow
Write-Host "使用Personal Access Token认证" -ForegroundColor Yellow
Write-Host ""

# 切换到项目目录
Set-Location "d:\qodercode"

try {
    # 1. 添加所有文件
    Write-Host "1️⃣ 添加文件到暂存区..." -ForegroundColor Cyan
    git add .
    Write-Host "✅ 文件已添加" -ForegroundColor Green
    
    # 2. 提交更改
    Write-Host "`n2️⃣ 提交更改..." -ForegroundColor Cyan
    $commitMessage = @"
完善六年级词库，添加GitHub同步功能

- 新增完整的六年级词库文件
- 添加GitHub Token认证支持
- 解决词库不完整问题
- 词库来源：2024年人教版PEP教材
"@
    
    git commit -m $commitMessage
    Write-Host "✅ 提交完成" -ForegroundColor Green
    
    # 3. 使用Token推送
    Write-Host "`n3️⃣ 推送到GitHub..." -ForegroundColor Cyan
    $tokenUrl = "https://firezxv123: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@github.com/firezxv123/english-word-app.git"
    
    git push $tokenUrl main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n🎉 推送成功！" -ForegroundColor Green
        Write-Host "🔗 查看项目: https://github.com/firezxv123/english-word-app" -ForegroundColor Blue
        
        Write-Host "`n📋 最新提交记录:" -ForegroundColor Yellow
        git log --oneline -n 3
        
    } else {
        Write-Host "`n❌ 推送失败" -ForegroundColor Red
        Write-Host "💡 请检查Token和网络连接" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "❌ 发生错误: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n🏁 操作完成" -ForegroundColor Green
Read-Host "按任意键退出"