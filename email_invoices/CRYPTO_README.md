# RSA 4096位加密配置说明

本项目使用RSA 4096位非对称加密来保护配置文件中的敏感信息（密码字段）。

## 加密原理

- **私钥加密，公钥解密**：使用私钥对密码进行加密，使用公钥进行解密
- **RSA 4096位**：采用4096位密钥长度，提供高安全性
- **OAEP填充**：使用OAEP（Optimal Asymmetric Encryption Padding）填充方案

## 文件说明

- `crypto_utils.py` - RSA加密工具类
- `setup_crypto.py` - 加密设置脚本
- `private_key.pem` - 私钥文件（自动生成）
- `public_key.pem` - 公钥文件（自动生成）

## 使用方法

### 1. 首次设置加密

```bash
# 进入email_invoices目录
cd email_invoices

# 运行加密设置脚本
python setup_crypto.py setup
```

这将：
- 生成RSA 4096位密钥对
- 加密配置文件中的密码字段
- 保存密钥文件到当前目录

### 2. 验证加密设置

```bash
python setup_crypto.py verify
```

### 3. 查看帮助

```bash
python setup_crypto.py help
```

## 安全注意事项

### 私钥安全
- **私钥文件 (`private_key.pem`) 必须妥善保管**
- 不要将私钥文件提交到版本控制系统
- 不要将私钥文件分享给他人
- 建议将私钥文件放在安全的位置

### 公钥分发
- 公钥文件 (`public_key.pem`) 可以安全分发
- 公钥用于加密数据，无法用于解密

### 配置文件
- 加密后的配置文件可以安全存储
- 即使配置文件被泄露，没有私钥也无法解密密码

## 加密的字段

配置文件中的以下字段会被加密：

1. **email.password** - 邮箱密码
2. **proxy.password** - 代理密码（如果启用）

## 示例

### 加密前的配置文件
```json
{
    "email": {
        "server": "imap.163.com",
        "port": 993,
        "username": "example@qq.com",
        "password": "your_password_here",
        "use_ssl": true
    }
}
```

### 加密后的配置文件
```json
{
    "email": {
        "server": "imap.163.com",
        "port": 993,
        "username": "example@qq.com",
        "password": "eyJ0eXBlIjogIk9BRVAiLCAiYWxnb3JpdGhtIjogIlJTQSIsICJrZXlfc2l6ZSI6IDQwOTYsICJkYXRhIjogImxvbmdfZW5jcnlwdGVkX3N0cmluZ19oZXJlIn0=",
        "use_ssl": true
    }
}
```

## 程序运行

程序运行时会自动：
1. 加载私钥文件
2. 解密配置文件中的密码字段
3. 使用解密后的密码进行邮箱连接

如果私钥文件不存在或解密失败，程序会提示错误并退出。

## 故障排除

### 问题：解密失败
**解决方案：**
1. 检查私钥文件是否存在
2. 确认私钥文件与加密时使用的私钥一致
3. 重新运行 `python setup_crypto.py setup`

### 问题：密钥文件丢失
**解决方案：**
1. 重新生成密钥对：`python setup_crypto.py setup`
2. 注意：使用新密钥加密后，之前加密的数据将无法解密

### 问题：配置文件损坏
**解决方案：**
1. 恢复备份的配置文件
2. 重新运行加密设置：`python setup_crypto.py setup`

## 技术细节

### 加密算法
- **算法**：RSA
- **密钥长度**：4096位
- **填充方案**：OAEP with SHA-256
- **编码**：Base64

### 密钥格式
- **私钥**：PEM格式，PKCS#8
- **公钥**：PEM格式，X.509 SubjectPublicKeyInfo

### 兼容性
- Python 3.8+
- cryptography库 41.0.0+ 