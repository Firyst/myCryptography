# -*- coding: utf-8 -*-
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import os
import importlib
from PyQt5 import QtGui
from time import sleep


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
        self.clear_button.clicked.connect(self.clear)

    def clear(self):
        """ Clear both fields """
        self.cipher_text_menu.setPlainText("")
        self.open_text_menu.setPlainText("")

    def load_modules(self):
        """ Load all cipher modules from ./cryptos/folder"""
        ind = 0
        module_list = [f for f in os.listdir("cryptos") if os.path.isfile(os.path.join("cryptos", f))]
        for module_name in module_list:
            try:
                sleep(0.1)
                module = importlib.import_module(f"cryptos.{module_name[:-3]}")
                self.modules[module.MODULE_NAME] = module.Crypto(self, ind)
                self.cipher_selector.addWidget(self.modules[module.MODULE_NAME])
                self.cipher_selector_box.addItem(module.MODULE_NAME)
                ind += 1
            except Exception as e:
                print(e)

    def open_text(self) -> str:
        """ Returns current open text"""
        return self.open_text_menu.toPlainText()

    def cipher_text(self) -> str:
        """ Return current cipher text"""
        return self.cipher_text_menu.toPlainText()

    def check_encryption(self):
        """ Check for non-empty open text area """
        if self.open_text():
            self.encrypt_button.setEnabled(1)
        else:
            self.encrypt_button.setEnabled(0)

    def check_decryption(self):
        """ Check for non-empty cipher text area """
        if self.cipher_text():
            self.decrypt_button.setEnabled(1)
        else:
            self.decrypt_button.setEnabled(0)

    def change_crypto(self):
        """ Open settings menu for selected cipher method"""
        self.cipher_selector.setCurrentIndex(self.get_current_module().page)
        if self.get_current_module().SUPPORTS_PUNC:
            self.punctuation.setEnabled(1)
            self.punctuation.setToolTip("")
        else:
            self.punctuation.setEnabled(0)
            self.punctuation.setToolTip("Данный шифр не поддерживает опцию")

    def get_current_module(self):
        """ Returns currently selected cipher module """
        return self.modules[self.cipher_selector_box.currentText()]

    def encrypt(self):
        """ Calls encrypt from cipher module and sets the result text """
        encrypted_text = self.get_current_module().encrypt()
        self.cipher_text_menu.setPlainText(encrypted_text)

    def decrypt(self):
        """ Calls decrypt from cipher module and sets the result text """
        decrypted_text = self.get_current_module().decrypt()
        self.open_text_menu.setPlainText(decrypted_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont("resources/Hack-Regular.ttf")  # load font
    win = ProgramWindow()
    win.show()
    sys.exit(app.exec_())
