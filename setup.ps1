# Auto Invoice - UV Setup Script
# 自动发票项目 - UV环境初始化脚本

Write-Host "正在初始化 Auto Invoice 项目的 UV 环境..." -ForegroundColor Green

# 检查是否安装了uv
try {
    $uvVersion = uv --version
    Write-Host "检测到 UV 版本: $uvVersion" -ForegroundColor Green
} catch {
    Write-Host "未检测到 UV，正在安装..." -ForegroundColor Yellow
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    Write-Host "UV 安装完成！" -ForegroundColor Green
}

# 创建虚拟环境并安装依赖
Write-Host "正在创建虚拟环境并安装依赖..." -ForegroundColor Yellow
uv sync --extra dev

# 安装playwright浏览器
Write-Host "正在安装 Playwright 浏览器..." -ForegroundColor Yellow
uv run playwright install chrome

Write-Host "环境初始化完成！" -ForegroundColor Green
Write-Host ""
Write-Host "使用方法:" -ForegroundColor Cyan
Write-Host "1. 编辑 email_invoices/config.json 配置邮箱信息" -ForegroundColor White
Write-Host "2. 运行: uv run python email_invoices/run_bot.py" -ForegroundColor White
Write-Host "3. 运行测试: uv run pytest" -ForegroundColor White
Write-Host "4. 代码格式化: uv run black email_invoices/" -ForegroundColor White 