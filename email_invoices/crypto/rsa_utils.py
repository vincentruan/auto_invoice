import base64
import os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend

class RSACrypto:
    """RSA 4096位非对称加密工具类"""
    def __init__(self, private_key_path=None, public_key_path=None):
        base_dir = os.path.dirname(__file__)
        self.private_key_path = private_key_path or os.path.join(base_dir, "private_key.pem")
        self.public_key_path = public_key_path or os.path.join(base_dir, "public_key.pem")
        self.private_key = None
        self.public_key = None

    def generate_key_pair(self):
        """生成RSA 4096位密钥对"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        with open(self.private_key_path, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        with open(self.public_key_path, "wb") as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
        print(f"密钥对已生成:")
        print(f"私钥: {self.private_key_path}")
        print(f"公钥: {self.public_key_path}")
        return private_key, public_key

    def load_keys(self):
        """加载密钥对"""
        if not os.path.exists(self.private_key_path) or not os.path.exists(self.public_key_path):
            print("密钥文件不存在，正在生成新的密钥对...")
            return self.generate_key_pair()
        with open(self.private_key_path, "rb") as f:
            self.private_key = serialization.load_pem_private_key(
                f.read(),
                password=None,
                backend=default_backend()
            )
        with open(self.public_key_path, "rb") as f:
            self.public_key = serialization.load_pem_public_key(
                f.read(),
                backend=default_backend()
            )
        return self.private_key, self.public_key

    def encrypt(self, data):
        """使用公钥加密数据"""
        if not self.public_key:
            self.load_keys()
        if isinstance(data, str):
            data = data.encode('utf-8')
        encrypted_data = self.public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return base64.b64encode(encrypted_data).decode('utf-8')

    def decrypt(self, encrypted_data):
        """使用私钥解密数据"""
        if not self.private_key:
            self.load_keys()
        encrypted_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
        decrypted_data = self.private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_data.decode('utf-8') 