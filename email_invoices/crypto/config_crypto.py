import json
from .rsa_utils import RSACrypto

class ConfigCrypto:
    """配置文件加密工具类"""
    def __init__(self, config_path="config/config.json", private_key_path=None, public_key_path=None):
        self.config_path = config_path
        self.crypto = RSACrypto(private_key_path=private_key_path, public_key_path=public_key_path)

    def encrypt_config(self):
        """加密配置文件中的密码字段"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        if 'password' in config['email']:
            config['email']['password'] = self.crypto.encrypt(config['email']['password'])
        if 'proxy' in config and 'password' in config['proxy']:
            config['proxy']['password'] = self.crypto.encrypt(config['proxy']['password'])
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        print("配置文件密码字段已加密")

    def decrypt_config(self):
        """解密配置文件中的密码字段"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        if 'password' in config['email']:
            try:
                config['email']['password'] = self.crypto.decrypt(config['email']['password'])
            except Exception as e:
                print(f"解密email密码失败: {e}")
                return None
        if 'proxy' in config and 'password' in config['proxy']:
            try:
                config['proxy']['password'] = self.crypto.decrypt(config['proxy']['password'])
            except Exception as e:
                print(f"解密proxy密码失败: {e}")
                return None
        return config 