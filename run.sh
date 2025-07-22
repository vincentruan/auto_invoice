#!/bin/bash

# Auto Invoice - 运行脚本
# 自动发票项目 - 运行程序

echo "=== Auto Invoice 运行脚本 ==="

# 检查是否在正确的目录
if [ ! -f "email_invoices/config.json" ]; then
    echo "错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 检查配置文件
if [ ! -f "email_invoices/config.json" ]; then
    echo "错误: 配置文件不存在，请先配置邮箱信息"
    echo "编辑 email_invoices/config.json 文件"
    exit 1
fi

echo "正在启动自动发票下载程序..."

# 使用uv运行程序
if uv run python email_invoices/run_bot.py; then
    echo "程序执行完成！"
else
    echo "程序执行出错，请检查配置文件和网络连接"
    exit 1
fi 