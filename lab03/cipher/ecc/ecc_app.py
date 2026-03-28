import sys
import os
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
# Thêm đường dẫn để import được thư mục ui
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from ui.ecc_ui import Ui_MainWindow # Đảm bảo tên class khớp với file ecc_ui.py

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.base_url = "http://127.0.0.1:5000/api/ecc"
        
        self.ui.btn_gen_keys.clicked.connect(self.call_api_gen_keys)
        self.ui.btn_sign.clicked.connect(self.call_api_sign)
        self.ui.btn_verify.clicked.connect(self.call_api_verify)

    def call_api_gen_keys(self):
        try:
            res = requests.get(f"{self.base_url}/generate_keys")
            QMessageBox.information(self, "Thông báo", res.json()['message'])
        except: QMessageBox.critical(self, "Lỗi", "Không thể kết nối Server!")

    def call_api_sign(self):
        msg = self.ui.txt_info.toPlainText()
        res = requests.post(f"{self.base_url}/sign", json={"message": msg})
        self.ui.txt_sign.setPlainText(res.json()['signature'])
        QMessageBox.information(self, "Thông báo", "Đã ký thành công!")

    def call_api_verify(self):
        msg = self.ui.txt_info.toPlainText()
        sig = self.ui.txt_sign.toPlainText()
        res = requests.post(f"{self.base_url}/verify", json={"message": msg, "signature": sig})
        if res.json()['is_verified']:
            QMessageBox.information(self, "Kết quả", "Xác minh thành công!")
        else:
            QMessageBox.warning(self, "Kết quả", "Xác minh thất bại!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())