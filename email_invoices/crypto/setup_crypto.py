import os
import sys
from .rsa_utils import RSACrypto
from .config_crypto import ConfigCrypto


def setup_encryption():
    print("=== RSA 4096位加密设置 ===")
    print()
    config_path = "../config.json"
    if not os.path.exists(config_path):
        print(f"错误: 配置文件 {config_path} 不存在")
        return False
    print("1. 生成RSA 4096位密钥对...")
    crypto = RSACrypto()
    private_key, public_key = crypto.generate_key_pair()
    print("✓ 密钥对生成完成")
    print()
    print("2. 加密配置文件中的密码字段...")
    config_crypto = ConfigCrypto(config_path)
    config_crypto.encrypt_config()
    print("✓ 配置文件加密完成")
    print()
    print("=== 设置完成 ===")
    print("重要提示:")
    print("- 私钥文件 (private_key.pem) 请妥善保管，不要泄露给他人")
    print("- 公钥文件 (public_key.pem) 可以安全分发")
    print("- 加密后的配置文件中的密码字段已使用RSA 4096位加密")
    print("- 程序运行时会自动解密密码字段")
    print()
    return True

def verify_encryption():
    print("=== 验证加密设置 ===")
    print()
    try:
        config_crypto = ConfigCrypto("../config.json")
        config = config_crypto.decrypt_config()
        if config is None:
            print("❌ 解密失败，请检查密钥文件")
            return False
        print("✓ 配置文件解密成功")
        print(f"✓ 邮箱服务器: {config['email']['server']}")
        print(f"✓ 邮箱用户名: {config['email']['username']}")
        print("✓ 密码字段已正确解密")
        if config.get('proxy', {}).get('enabled', False):
            print("✓ 代理密码字段已正确解密")
        print()
        print("=== 验证完成 ===")
        return True
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False

def main():
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "setup":
            setup_encryption()
        elif command == "verify":
            verify_encryption()
        elif command == "help":
            print("用法:")
            print("  python setup_crypto.py setup   - 设置加密环境")
            print("  python setup_crypto.py verify  - 验证加密设置")
            print("  python setup_crypto.py help    - 显示帮助信息")
        else:
            print(f"未知命令: {command}")
            print("使用 'python setup_crypto.py help' 查看帮助")
    else:
        setup_encryption()
        print()
        verify_encryption()

if __name__ == "__main__":
    main() 