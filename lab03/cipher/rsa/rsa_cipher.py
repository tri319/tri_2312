import sys
import os
import requests
import rsa
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox

# Tự động thêm đường dẫn gốc để tìm thấy thư mục 'ui'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from ui.rsa_ui import Ui_Dialog 

# --- LỚP LOGIC (Để api.py import) ---
class RSACipher:
    def __init__(self):
        self.path = "cipher/rsa/keys/"
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def generate_keys(self):
        (pub_key, priv_key) = rsa.newkeys(1024)
        with open(self.path + "publicKey.pem", "wb") as f:
            f.write(pub_key.save_pkcs1())
        with open(self.path + "privateKey.pem", "wb") as f:
            f.write(priv_key.save_pkcs1())

    def load_keys(self):
        with open(self.path + "publicKey.pem", "rb") as f:
            pub_key = rsa.PublicKey.load_pkcs1(f.read())
        with open(self.path + "privateKey.pem", "rb") as f:
            priv_key = rsa.PrivateKey.load_pkcs1(f.read())
        return priv_key, pub_key

    def encrypt(self, message, pub_key):
        return rsa.encrypt(message.encode('utf-8'), pub_key)

    def decrypt(self, crypto, priv_key):
        return rsa.decrypt(crypto, priv_key).decode('utf-8')

# --- LỚP GIAO DIỆN ---
class RSAApp(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.base_url = "http://127.0.0.1:5000/api/rsa"
        # Kết nối sự kiện nút bấm
        self.btn_gen_keys.clicked.connect(self.call_api_gen_keys)
        self.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.btn_decrypt.clicked.connect(self.call_api_decrypt)
        self.btn_sign.clicked.connect(self.call_api_sign)
        self.btn_verify.clicked.connect(self.call_api_verify)

    def call_api_gen_keys(self):
        res = requests.get(f"{self.base_url}/generate_keys")
        QMessageBox.information(self, "Thông báo", res.json()['message'])

    def call_api_encrypt(self):
        msg = self.txt_plain_text.toPlainText()
        res = requests.post(f"{self.base_url}/encrypt", json={"message": msg})
        self.txt_cipher_text.setPlainText(res.json()['encrypted_message'])

    def call_api_decrypt(self):
        cipher = self.txt_cipher_text.toPlainText()
        res = requests.post(f"{self.base_url}/decrypt", json={"ciphertext": cipher})
        self.txt_plain_text.setPlainText(res.json()['decrypted_message'])

    def call_api_sign(self):
        msg = self.txt_info.toPlainText()
        res = requests.post(f"{self.base_url}/sign", json={"message": msg})
        self.txt_sign.setPlainText(res.json()['signature'])

    def call_api_verify(self):
        msg = self.txt_info.toPlainText()
        sig = self.txt_sign.toPlainText()
        res = requests.post(f"{self.base_url}/verify", json={"message": msg, "signature": sig})
        if res.json()['is_valid']:
            QMessageBox.information(self, "Kết quả", "Chữ ký HỢP LỆ!")
        else:
            QMessageBox.warning(self, "Kết quả", "Chữ ký SAI!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RSAApp()
    window.show()
    sys.exit(app.exec_())