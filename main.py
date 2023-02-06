# -*- coding: utf-8 -*-
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import os
import cryptos.basic_replace
import importlib
from PyQt5 import QtGui


class ProgramWindow(QMainWindow):
    """! Главное окно программы
    """
    def __init__(self):
        """! Инициализация окна
        """
        super().__init__()
        uic.loadUi('resources/Window.ui', self)

        self.modules = dict()  # name: object
        self.pages = dict()
        self.load_modules()

        self.setup_signals()

    def setup_signals(self):
        self.open_text_menu.textChanged.connect(self.check_encryption)
        self.cipher_text_menu.textChanged.connect(self.check_decryption)
        self.encrypt_button.clicked.connect(self.encrypt)
        self.decrypt_button.clicked.connect(self.decrypt)
        self.cipher_selector_box.currentIndexChanged.connect(self.change_crypto)

    def load_modules(self):
        ind = 0
        module_list = [f for f in os.listdir("cryptos") if os.path.isfile(os.path.join("cryptos", f))]
        for module_name in module_list:
            try:
                module = importlib.import_module(f"cryptos.{module_name[:-3]}")
                self.modules[module.MODULE_NAME] = module.Crypto(self, ind)
                self.cipher_selector.addWidget(self.modules[module.MODULE_NAME])
                self.cipher_selector_box.addItem(module.MODULE_NAME)
                ind += 1
            except Exception as e:
                print(e)

    def open_text(self) -> str:
        return self.open_text_menu.toPlainText()

    def cipher_text(self) -> str:
        return self.cipher_text_menu.toPlainText()

    def check_encryption(self):
        if self.open_text():
            self.encrypt_button.setEnabled(1)
        else:
            self.encrypt_button.setEnabled(0)

    def check_decryption(self):
        if self.cipher_text():
            self.decrypt_button.setEnabled(1)
        else:
            self.decrypt_button.setEnabled(0)

    def change_crypto(self):
        print(self.get_current_module().page)
        self.cipher_selector.setCurrentIndex(self.get_current_module().page)

    def get_current_module(self):
        return self.modules[self.cipher_selector_box.currentText()]

    def encrypt(self):
        encrypted_text = self.get_current_module().encrypt()
        self.cipher_text_menu.setPlainText(encrypted_text)

    def decrypt(self):
        decrypted_text = self.get_current_module().decrypt()
        self.open_text_menu.setPlainText(decrypted_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont("resources/Hack-Regular.ttf")  # load font
    win = ProgramWindow()
    win.show()
    sys.exit(app.exec_())
