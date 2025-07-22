#!/bin/bash

# Auto Invoice - UV Setup Script
# 自动发票项目 - UV环境初始化脚本

echo "正在初始化 Auto Invoice 项目的 UV 环境..."

# 检查是否安装了uv
if command -v uv &> /dev/null; then
    uv_version=$(uv --version)
    echo "检测到 UV 版本: $uv_version"
else
    echo "未检测到 UV，正在安装..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo "UV 安装完成！"
    # 重新加载shell配置
    source ~/.bashrc 2>/dev/null || source ~/.zshrc 2>/dev/null || true
fi

# 创建虚拟环境并安装依赖
echo "正在创建虚拟环境并安装依赖..."
uv sync --extra dev

# 安装playwright浏览器
echo "正在安装 Playwright 浏览器..."
uv run playwright install chrome

echo "环境初始化完成！"
echo ""
echo "使用方法:"
echo "1. 编辑 email_invoices/config.json 配置邮箱信息"
echo "2. 运行: uv run python email_invoices/run_bot.py"
echo "3. 运行测试: uv run pytest"
echo "4. 代码格式化: uv run black email_invoices/" 