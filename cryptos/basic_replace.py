from main import ProgramWindow

from dialogs import WarnDialog
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
MODULE_NAME = "Простая замена"


class Crypto(QWidget):
    def __init__(self, parent: ProgramWindow, page):
        super().__init__()
        uic.loadUi('resources/basic_replace.ui', self)
        self.parent_window = parent
        self.page = page
        print("init module basic replace")

        self.auto_button.clicked.connect(self.auto_alph)
        self.move_left_button.clicked.connect(self.move_left)
        self.move_right_button.clicked.connect(self.move_right)

    def auto_alph(self):
        alph = ''.join(sorted(list(set(self.parent_window.open_text()))))
        self.alph0.setText(alph)
        self.alph1.setText(alph)

    def move_left(self):
        text = self.alph1.text()
        if text:
            self.alph1.setText(text[1:] + text[0])

    def move_right(self):
        text = self.alph1.text()
        if text:
            self.alph1.setText(text[-1] + text[:-1])

    def encrypt(self):
        alph0, alph1 = self.alph0.text(), self.alph1.text()
        if len(alph0) == len(alph1):
            encrypted = ""
            replaces = dict(zip(alph0, alph1))
            s = "?"
            try:
                for s in self.parent_window.open_text():
                    encrypted += replaces[s]
            except KeyError:
                dialog = WarnDialog("Ошибка", f"Символ <{s}> отсутсвует в заданном алфавите.")
                dialog.exec_()
                return ""
            return encrypted
        else:
            dialog = WarnDialog("Ошибка", "Длина алфавитов не совпадает")
            dialog.exec_()
            return ''

    def decrypt(self):
        alph1, alph0 = self.alph0.text(), self.alph1.text()
        if len(alph0) == len(alph1):
            decrypted = ""
            replaces = dict(zip(alph0, alph1))
            s = "?"
            try:
                for s in self.parent_window.cipher_text():
                    decrypted += replaces[s]
            except KeyError:
                dialog = WarnDialog("Ошибка", f"Символ <{s}> отсутсвует в заданном алфавите.")
                dialog.exec_()
                return ""
            return decrypted
        else:
            dialog = WarnDialog("Ошибка", "Длина алфавитов не совпадает")
            dialog.exec_()
            return ''
