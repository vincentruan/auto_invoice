# Auto Invoice - 运行脚本
# 自动发票项目 - 运行程序

Write-Host "=== Auto Invoice 运行脚本 ===" -ForegroundColor Green

# 检查是否在正确的目录
if (-not (Test-Path "email_invoices/config.json")) {
    Write-Host "错误: 请在项目根目录运行此脚本" -ForegroundColor Red
    exit 1
}

# 检查配置文件
if (-not (Test-Path "email_invoices/config.json")) {
    Write-Host "错误: 配置文件不存在，请先配置邮箱信息" -ForegroundColor Red
    Write-Host "编辑 email_invoices/config.json 文件" -ForegroundColor Yellow
    exit 1
}

Write-Host "正在启动自动发票下载程序..." -ForegroundColor Yellow

try {
    # 使用uv运行程序
    uv run python email_invoices/run_bot.py
    
    Write-Host "程序执行完成！" -ForegroundColor Green
} catch {
    Write-Host "程序执行出错: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "请检查配置文件和网络连接" -ForegroundColor Yellow
} 