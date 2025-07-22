# Auto Invoice - 快速开始指南

## 🚀 5分钟快速开始

### 1. 安装 UV

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. 克隆项目

```bash
git clone <repository-url>
cd auto_invoice
```

### 3. 一键初始化 (推荐)

**Windows:**
```powershell
.\setup.ps1
```

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

### 4. 配置邮箱

编辑 `email_invoices/config.json`:

```json
{
    "email": {
        "server": "imap.163.com",
        "port": 993,
        "username": "your-email@example.com",
        "password": "your-password",
        "use_ssl": true
    }
}
```

### 5. 运行程序

```bash
# 使用示例脚本
uv run python example.py

# 或直接运行主程序
uv run python email_invoices/run_bot.py
```

## 📋 常用命令

```bash
# 安装依赖
uv sync

# 运行测试
uv run pytest

# 测试 Playwright Chrome 浏览器
uv run python test_playwright.py

# 代码格式化
uv run black email_invoices/

# 代码检查
uv run flake8 email_invoices/

# 运行示例
uv run python example.py
```

## 🔧 故障排除

### 问题1: UV 命令未找到
**解决方案:** 重新安装 UV 或重启终端

### 问题2: 邮箱连接失败
**解决方案:** 
- 检查邮箱配置是否正确
- 确认邮箱开启了IMAP服务
- 检查密码是否为应用专用密码

### 问题3: Playwright 浏览器问题
**解决方案:**
```bash
uv run playwright install chrome
```

## 📁 项目结构

```
auto_invoice/
├── email_invoices/          # 主要代码
│   ├── config.json         # 配置文件
│   ├── email_client.py     # 邮件客户端
│   ├── invoice_attachment_downloader.py  # 发票下载器
│   └── run_bot.py          # 主程序
├── pyproject.toml          # 项目配置
├── setup.ps1              # Windows 初始化脚本
├── setup.sh               # Linux/macOS 初始化脚本
└── example.py             # 使用示例
```

## 🎯 下一步

- 查看 [README.md](README.md) 了解详细功能
- 阅读 [示例说明.md](示例说明.md) 了解使用场景
- 运行测试确保环境正常: `uv run pytest` 