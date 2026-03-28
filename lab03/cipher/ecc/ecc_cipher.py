import ecdsa
import os

class ECCCipher:
    def __init__(self):
        self.path = "cipher/ecc/keys/"
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def generate_keys(self):
        # Tạo khóa riêng tư (Signing Key)
        sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        # Lấy khóa công khai (Verifying Key) từ khóa riêng
        vk = sk.get_verifying_key()
        
        with open(self.path + "privateKey.pem", "wb") as f:
            f.write(sk.to_pem())
        with open(self.path + "publicKey.pem", "wb") as f:
            f.write(vk.to_pem())

    def load_keys(self):
        with open(self.path + "privateKey.pem", "rb") as f:
            sk = ecdsa.SigningKey.from_pem(f.read())
        with open(self.path + "publicKey.pem", "rb") as f:
            vk = ecdsa.VerifyingKey.from_pem(f.read())
        return sk, vk

    def sign(self, message, sk):
        # Ký dữ liệu
        return sk.sign(message.encode('utf-8'))

    def verify(self, message, signature, vk):
        # Xác minh chữ ký
        try:
            return vk.verify(signature, message.encode('utf-8'))
        except ecdsa.BadSignatureError:
            return False