# 依赖管理说明

## 🎯 为什么只使用 pyproject.toml？

本项目采用现代化的 Python 依赖管理方式，只使用 `pyproject.toml` 文件，原因如下：

### ✅ 优势

1. **标准化**: `pyproject.toml` 是 PEP 518 标准，是 Python 项目的未来
2. **功能完整**: 支持项目元数据、构建配置、工具配置等
3. **uv 原生支持**: uv 工具链完全基于 `pyproject.toml`
4. **减少冗余**: 避免维护多个依赖文件
5. **更好的依赖解析**: 支持可选依赖、开发依赖等

### 📋 依赖管理方式

#### 生产依赖
```toml
[project]
dependencies = [
    "imapclient>=2.1.0",
    "requests>=2.28.0",
    "playwright>=1.40.0",
    "pytest>=7.0.0",
]
```

#### 开发依赖
```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "black>=23.0.0",
    "flake8>=6.0.0",
]
```

### 🚀 使用方法

#### 安装生产依赖
```bash
uv sync
```

#### 安装开发依赖
```bash
uv sync --extra dev
```

#### 添加新依赖
```bash
uv add package-name
uv add --dev package-name  # 开发依赖
```

#### 移除依赖
```bash
uv remove package-name
```

### 🔄 与传统方式的对比

| 特性 | pyproject.toml | requirements.txt |
|------|----------------|------------------|
| 标准化 | ✅ PEP 518 标准 | ❌ 非标准格式 |
| 元数据支持 | ✅ 完整支持 | ❌ 不支持 |
| 可选依赖 | ✅ 支持 | ❌ 不支持 |
| 构建配置 | ✅ 支持 | ❌ 不支持 |
| 工具配置 | ✅ 支持 | ❌ 不支持 |
| uv 支持 | ✅ 原生支持 | ⚠️ 兼容支持 |

### 📝 迁移指南

如果您需要从 `requirements.txt` 迁移：

1. **导出当前依赖**
   ```bash
   uv pip freeze > requirements.txt
   ```

2. **转换为 pyproject.toml 格式**
   ```toml
   [project]
   dependencies = [
       "package1>=1.0.0",
       "package2>=2.0.0",
   ]
   ```

3. **删除 requirements.txt**
   ```bash
   rm requirements.txt
   ```

### 🎯 最佳实践

1. **使用 uv 管理依赖**: `uv add`, `uv remove`, `uv sync`
2. **锁定版本**: `uv.lock` 文件确保环境一致性
3. **分离开发依赖**: 使用 `[project.optional-dependencies]`
4. **定期更新**: `uv lock --upgrade` 更新依赖版本

### ❓ 常见问题

**Q: 如果某个平台不支持 pyproject.toml 怎么办？**
A: 可以使用 `uv pip freeze > requirements.txt` 临时生成

**Q: 如何查看当前安装的依赖？**
A: `uv pip list` 或 `uv pip freeze`

**Q: 如何更新所有依赖？**
A: `uv lock --upgrade` 然后 `uv sync`

### 🌐 Playwright 浏览器配置

本项目使用 **Chrome** 作为 Playwright 的默认浏览器：

#### 安装 Chrome 浏览器
```bash
uv run playwright install chrome
```

#### 代码中的浏览器配置
```python
# 使用 Chromium (Chrome 内核)
browser = playwright.chromium.launch(headless=False)
```

#### 为什么选择 Chrome？
- **更好的兼容性**: Chrome 内核对现代网页支持更好
- **更快的性能**: Chrome 在自动化场景下性能更优
- **更稳定的 API**: Chrome 的 Playwright API 更稳定
- **更小的安装包**: Chrome 安装包相对较小 