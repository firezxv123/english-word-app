# GitHub提交指南
# 使用您的凭据：用户名 firezxv123，Token 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

## 方式一：直接在命令行执行（推荐）

# 1. 打开命令提示符或PowerShell，进入项目目录
cd d:\qodercode

# 2. 添加所有文件
git add .

# 3. 提交更改
git commit -m "完善六年级词库，添加GitHub同步功能

- 新增完整的六年级词库文件
- 添加GitHub Token认证支持
- 解决词库不完整问题
- 词库来源：2024年人教版PEP教材"

# 4. 使用Token推送（一行命令）
git push https://firezxv123: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@github.com/firezxv123/english-word-app.git main

## 方式二：配置远程仓库后推送

# 1. 设置远程仓库URL（包含Token）
git remote set-url origin https://firezxv123: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@github.com/firezxv123/english-word-app.git

# 2. 推送到GitHub
git push -u origin main

# 3. 恢复原始URL（安全起见）
git remote set-url origin https://github.com/firezxv123/english-word-app.git

## 方式三：使用Git凭据管理器

# 1. 配置Git使用Token
git config --global user.name "firezxv123"
git config --global user.email "dev@example.com"

# 2. 推送时会提示输入用户名和密码
git push origin main
# 用户名：firezxv123
# 密码：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

## 验证推送成功

# 检查最新提交
git log --oneline -n 3

# 查看远程分支
git branch -r

# 访问GitHub查看：https://github.com/firezxv123/english-word-app

## 注意事项

1. Token具有完整的仓库访问权限
2. 推送成功后，Token会被Git记住（在凭据管理器中）
3. 如果仓库不存在，需要先在GitHub创建
4. 确保网络连接正常，能访问GitHub

## 故障排除

如果推送失败，可能的原因：
1. Token已过期或被撤销
2. 仓库不存在或无权限
3. 网络连接问题
4. 分支保护规则限制

解决方案：
1. 检查Token有效性
2. 确认仓库存在
3. 尝试使用SSH方式
4. 检查防火墙设置