.PHONY: install install-dev lock sync test lint format clean

# 安装生产依赖
install:
	uv pip install -e .

# 安装开发依赖
install-dev:
	uv pip install -e ".[dev]"

# 锁定依赖版本
lock:
	uv lock

# 同步依赖
sync:
	uv sync

# 运行测试
test:
	uv run pytest

# 测试 Playwright Chrome 浏览器
test-playwright:
	uv run python test_playwright.py

# 代码检查
lint:
	uv run flake8 email_invoices/
	uv run black --check email_invoices/

# 代码格式化
format:
	uv run black email_invoices/

# 清理缓存
clean:
	uv cache clean
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete 