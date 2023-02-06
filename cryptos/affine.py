from main import ProgramWindow
import math
from dialogs import WarnDialog
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
MODULE_NAME = "Аффинный"


class Crypto(QWidget):
    def __init__(self, parent: ProgramWindow, page):
        super().__init__()
        uic.loadUi('resources/affine.ui', self)
        self.parent_window = parent
        self.page = page
        print("init module affine")

        self.auto_button.clicked.connect(self.auto_alph)

    def auto_alph(self):
        alph = ''.join(sorted(list(set(self.parent_window.open_text()))))
        self.alph0.setText(alph)

    def move_left(self):
        text = self.alph1.text()
        if text:
            self.alph1.setText(text[1:] + text[0])

    def move_right(self):
        text = self.alph1.text()
        if text:
            self.alph1.setText(text[-1] + text[:-1])

    def decrypt(self):
        alph = list(self.alph0.text())
        alph_rev = dict(zip(alph, range(len(alph))))  # создать обратный словарь для более быстрой работы
        try:
            a, b = int(self.key_a.value()), int(self.key_b.value())
            ia = pow(a, -1, len(alph))
        except ValueError:
            dialog = WarnDialog("Ошибка", "Ключи заданы неверно")
            dialog.exec_()
            return ''
        if math.gcd(len(alph), a) == 1:
            # crypto begin
            decrypted = ""
            s = "?"
            try:
                for s in self.parent_window.cipher_text():
                    decrypted += alph[((alph_rev[s] - b) * ia) % len(alph)]  # формула
            except KeyError:
                dialog = WarnDialog("Ошибка", f"Символ <{s}> отсутсвует в заданном алфавите.")
                dialog.exec_()
                return ""
            return decrypted
        else:
            dialog = WarnDialog("Ошибка", "Числа a и m должны быть взаимно простыми")
            dialog.exec_()
            return ''

    def encrypt(self):
        alph = list(self.alph0.text())
        alph_rev = dict(zip(alph, range(len(alph))))  # создать обратный словарь для более быстрой работы
        print(alph, alph_rev)
        try:
            a, b = int(self.key_a.value()), int(self.key_b.value())
        except ValueError:
            dialog = WarnDialog("Ошибка", "Ключи заданы неверно")
            dialog.exec_()
            return ''
        if math.gcd(len(alph), a) == 1:
            # crypto begin
            encrypted = ""
            s = "?"
            try:
                for s in self.parent_window.open_text():
                    encrypted += alph[(alph_rev[s] * a + b) % len(alph)]  # формула
            except KeyError:
                dialog = WarnDialog("Ошибка", f"Символ <{s}> отсутсвует в заданном алфавите.")
                dialog.exec_()
                return ""
            return encrypted
        else:
            dialog = WarnDialog("Ошибка", "Числа a и m должны быть взаимно простыми")
            dialog.exec_()
            return ''
