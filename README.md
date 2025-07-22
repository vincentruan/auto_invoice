# Auto Invoice

自动下载邮件中的发票附件的Python项目。

## 功能特性

- 自动连接邮件服务器并获取发票邮件
- 下载邮件附件中的PDF发票
- 从邮件正文中提取发票下载链接并下载
- 使用Playwright进行浏览器自动化下载
- 按日期组织下载的发票文件

## 环境要求

- Python 3.8+
- uv (Python包管理器)

## 安装

### 1. 安装uv

```bash
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. 克隆项目

```bash
git clone <repository-url>
cd auto_invoice
```

### 3. 安装依赖

```bash
# 安装生产依赖
uv sync

# 或者安装开发依赖（包含测试和代码格式化工具）
uv sync --extra dev
```

## 使用方法

### 1. 配置邮箱

编辑 `email_invoices/config.json` 文件，配置您的邮箱信息：

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

### 2. 运行程序

```bash
# 使用uv运行
uv run python email_invoices/run_bot.py

# 或者直接运行
python email_invoices/run_bot.py
```

## 开发

### 常用命令

```bash
# 安装开发依赖
make install-dev

# 运行测试
make test

# 代码格式化
make format

# 代码检查
make lint

# 锁定依赖版本
make lock

# 同步依赖
make sync

# 清理缓存
make clean
```

### 项目结构

```
auto_invoice/
├── email_invoices/
│   ├── __init__.py
│   ├── config.json              # 配置文件
│   ├── email_client.py          # 邮件客户端
│   ├── invoice_attachment_downloader.py  # 发票下载器
│   ├── run_bot.py               # 主程序
│   ├── run.bat                  # Windows批处理文件
│   └── tests/
│       └── test_email_client.py # 测试文件
├── pyproject.toml               # 项目配置
├── uv.lock                      # 依赖锁定文件
├── Makefile                     # 构建脚本
└── README.md                    # 项目说明
```

## 依赖管理

本项目使用 [uv](https://github.com/astral-sh/uv) 作为Python包管理器，它比pip更快、更可靠。

### 主要依赖

- `imapclient`: IMAP邮件客户端
- `requests`: HTTP请求库
- `playwright`: 浏览器自动化
- `pytest`: 测试框架

### 开发依赖

- `pytest-cov`: 测试覆盖率
- `black`: 代码格式化
- `flake8`: 代码检查

## 许可证

BSD 3-Clause License