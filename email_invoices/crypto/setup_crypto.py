import os
import sys
from .rsa_utils import RSACrypto
from .config_crypto import ConfigCrypto


def setup_encryption(config_path=None, private_key_path=None, public_key_path=None):
    print("=== RSA 4096位加密设置 ===")
    print()
    # 默认路径
    config_path = config_path or os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "config.json")
    private_key_path = private_key_path or os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "private_key.pem")
    public_key_path = public_key_path or os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "public_key.pem")
    if not os.path.exists(config_path):
        print(f"错误: 配置文件 {config_path} 不存在")
        return False
    print("1. 生成RSA 4096位密钥对...")
    crypto = RSACrypto(private_key_path=private_key_path, public_key_path=public_key_path)
    private_key, public_key = crypto.generate_key_pair()
    print("✓ 密钥对生成完成")
    print()
    print("2. 加密配置文件中的密码字段...")
    config_crypto = ConfigCrypto(config_path, private_key_path, public_key_path)
    config_crypto.encrypt_config()
    print("✓ 配置文件加密完成")
    print()
    print("=== 设置完成 ===")
    print("重要提示:")
    print(f"- 私钥文件: {private_key_path} 请妥善保管，不要泄露给他人")
    print(f"- 公钥文件: {public_key_path} 可以安全分发")
    print("- 加密后的配置文件中的密码字段已使用RSA 4096位加密")
    print("- 程序运行时会自动解密密码字段")
    print()
    return True

def verify_encryption(config_path=None, private_key_path=None, public_key_path=None):
    print("=== 验证加密设置 ===")
    print()
    config_path = config_path or os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "config.json")
    private_key_path = private_key_path or os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "private_key.pem")
    public_key_path = public_key_path or os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "public_key.pem")
    try:
        config_crypto = ConfigCrypto(config_path, private_key_path, public_key_path)
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
    import argparse
    parser = argparse.ArgumentParser(description="RSA加密配置工具")
    parser.add_argument('--config', type=str, default=None, help='配置文件路径，默认config/config.json')
    parser.add_argument('--private', type=str, default=None, help='私钥路径，默认config/private_key.pem')
    parser.add_argument('--public', type=str, default=None, help='公钥路径，默认config/public_key.pem')
    parser.add_argument('command', nargs='?', default='setup', choices=['setup', 'verify', 'help'], help='操作命令')
    args = parser.parse_args()
    if args.command == "setup":
        setup_encryption(args.config, args.private, args.public)
    elif args.command == "verify":
        verify_encryption(args.config, args.private, args.public)
    elif args.command == "help":
        print("用法:")
        print("  python -m email_invoices.crypto.setup_crypto setup [--config path] [--private path] [--public path]")
        print("  python -m email_invoices.crypto.setup_crypto verify [--config path] [--private path] [--public path]")
        print("  python -m email_invoices.crypto.setup_crypto help")

if __name__ == "__main__":
    main() 