#!/usr/bin/env python3
"""
RSA加密功能演示脚本
展示如何使用RSA 4096位加密来保护配置文件中的密码字段
"""

import json
import os
from email_invoices.crypto.rsa_utils import RSACrypto
from email_invoices.crypto.config_crypto import ConfigCrypto


def demo_encryption_workflow():
    """演示完整的加密工作流程"""
    print("=== RSA 4096位加密演示 ===")
    print()
    
    # 1. 创建示例配置文件
    print("1. 创建示例配置文件...")
    example_config = {
        "email": {
            "server": "imap.163.com",
            "port": 993,
            "username": "vincenti18n@qq.com",
            "password": "qkdykbdhsmafbfgi",  # 原始密码
            "use_ssl": True
        },
        "proxy": {
            "enabled": False,
            "server": "proxy.example.com",
            "port": 8080,
            "username": "proxy_username",
            "password": "proxy_password"  # 原始密码
        }
    }
    
    # 保存示例配置
    with open("example_config.json", "w", encoding="utf-8") as f:
        json.dump(example_config, f, indent=4, ensure_ascii=False)
    
    print("✓ 示例配置文件已创建: example_config.json")
    print()
    
    # 2. 生成RSA密钥对
    print("2. 生成RSA 4096位密钥对...")
    crypto = RSACrypto("demo_private_key.pem", "demo_public_key.pem")
    private_key, public_key = crypto.generate_key_pair()
    print("✓ 密钥对已生成:")
    print("  - 私钥: demo_private_key.pem")
    print("  - 公钥: demo_public_key.pem")
    print()
    
    # 3. 加密配置文件
    print("3. 加密配置文件中的密码字段...")
    config_crypto = ConfigCrypto("example_config.json")
    config_crypto.encrypt_config()
    
    # 读取加密后的配置
    with open("example_config.json", "r", encoding="utf-8") as f:
        encrypted_config = json.load(f)
    
    print("✓ 密码字段已加密:")
    print(f"  - Email密码: {encrypted_config['email']['password'][:50]}...")
    print(f"  - 代理密码: {encrypted_config['proxy']['password'][:50]}...")
    print()
    
    # 4. 演示解密过程
    print("4. 演示解密过程...")
    decrypted_config = config_crypto.decrypt_config()
    
    if decrypted_config:
        print("✓ 解密成功:")
        print(f"  - Email密码: {decrypted_config['email']['password']}")
        print(f"  - 代理密码: {decrypted_config['proxy']['password']}")
        print()
        
        # 验证解密结果
        email_match = decrypted_config['email']['password'] == example_config['email']['password']
        proxy_match = decrypted_config['proxy']['password'] == example_config['proxy']['password']
        
        if email_match and proxy_match:
            print("✓ 验证通过: 解密后的密码与原始密码一致")
        else:
            print("❌ 验证失败: 解密后的密码与原始密码不一致")
    else:
        print("❌ 解密失败")
    
    print()
    print("=== 演示完成 ===")


def show_security_features():
    """展示安全特性"""
    print("=== 安全特性说明 ===")
    print()
    
    print("🔐 RSA 4096位非对称加密:")
    print("  - 密钥长度: 4096位")
    print("  - 加密方式: 私钥加密，公钥解密")
    print("  - 填充方案: OAEP with SHA-256")
    print("  - 编码格式: Base64")
    print()
    
    print("🛡️ 安全优势:")
    print("  - 即使配置文件被泄露，没有私钥也无法解密")
    print("  - 私钥文件可以单独保管，提高安全性")
    print("  - 支持密钥轮换，定期更换密钥对")
    print("  - 符合企业级安全标准")
    print()
    
    print("📁 文件管理:")
    print("  - 私钥文件 (.pem) 已添加到 .gitignore")
    print("  - 加密后的配置文件可以安全存储")
    print("  - 支持多环境部署，每个环境使用不同密钥")
    print()


def show_usage_instructions():
    """显示使用说明"""
    print("=== 使用说明 ===")
    print()
    
    print("🚀 快速开始:")
    print("1. 安装依赖: pip install cryptography>=41.0.0")
    print("2. 设置加密: python setup_crypto.py setup")
    print("3. 验证设置: python setup_crypto.py verify")
    print("4. 运行程序: python run_bot.py")
    print()
    
    print("🔧 管理命令:")
    print("  python setup_crypto.py setup   - 设置加密环境")
    print("  python setup_crypto.py verify  - 验证加密设置")
    print("  python setup_crypto.py help    - 显示帮助")
    print("  python test_crypto.py          - 运行测试")
    print()
    
    print("⚠️ 重要提醒:")
    print("  - 私钥文件必须妥善保管，不要泄露")
    print("  - 定期备份私钥文件")
    print("  - 生产环境建议使用更强的密钥保护措施")
    print()


def main():
    """主函数"""
    print("RSA 4096位加密功能演示")
    print("=" * 50)
    print()
    
    try:
        # 检查cryptography库是否可用
        import cryptography
        print("✓ cryptography库已安装")
        print()
        
        # 运行演示
        demo_encryption_workflow()
        print()
        show_security_features()
        print()
        show_usage_instructions()
        
    except ImportError:
        print("❌ cryptography库未安装")
        print("请运行以下命令安装:")
        print("  pip install cryptography>=41.0.0")
        print()
        print("或者使用uv:")
        print("  uv add cryptography>=41.0.0")
        print()
        show_usage_instructions()


if __name__ == "__main__":
    main() 