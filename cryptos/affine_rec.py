from main import ProgramWindow
import math
from dialogs import WarnDialog
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
MODULE_NAME = "Аффинный рек."


class Crypto(QWidget):
    def __init__(self, parent: ProgramWindow, page):
        super().__init__()
        uic.loadUi('resources/affine_rec.ui', self)
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

    def decrypt(self) -> str:
        """Decrypt function, will be called automatically"""
        alph = list(self.alph0.text())
        alph_rev = dict(zip(alph, range(len(alph))))  # reversed alphabet
        try:
            # load keys
            a1, b1 = int(self.key_a1.value()), int(self.key_b1.value())
            a2, b2 = int(self.key_a1.value()), int(self.key_b1.value())
        except ValueError:
            dialog = WarnDialog("Ошибка", "Ключи заданы неверно")
            dialog.exec_()
            return ''
        if math.gcd(len(alph), a1) and math.gcd(len(alph), a2) == 1:
            # crypto begin
            decrypted = ""
            s = "?"
            try:
                keys = [(a1, b1), (a2, b2)]
                for i, s in enumerate(self.parent_window.cipher_text()):
                    if i < 2:
                        a, b = keys[i][0], keys[i][1]
                    else:
                        a, b = keys[i - 1][0] * keys[i - 2][0], keys[i - 1][0] + keys[i - 2][0]  # generate new keys
                        keys.append((a, b))
                    ia = pow(a, -1, len(alph))  # inverted by module
                    decrypted += alph[((alph_rev[s] - b) * ia) % len(alph)]  # cipher formula

            except KeyError:
                dialog = WarnDialog("Ошибка", f"Символ <{s}> отсутсвует в заданном алфавите.")
                dialog.exec_()
                return ""
            return decrypted
        else:
            dialog = WarnDialog("Ошибка", "Числа a1, a2 и m должны быть взаимно простыми")
            dialog.exec_()
            return ''

    def encrypt(self) -> str:
        alph = list(self.alph0.text())
        alph_rev = dict(zip(alph, range(len(alph))))  # reversed alphabet
        try:
            # load keys
            a1, b1 = int(self.key_a1.value()), int(self.key_b1.value())
            a2, b2 = int(self.key_a1.value()), int(self.key_b1.value())
        except ValueError:
            dialog = WarnDialog("Ошибка", "Ключи заданы неверно")
            dialog.exec_()
            return ''
        if math.gcd(len(alph), a1) and math.gcd(len(alph), a2) == 1:
            # crypto begin
            encrypted = ""
            s = "?"
            try:
                keys = [(a1, b1), (a2, b2)]
                for i, s in enumerate(self.parent_window.open_text()):
                    if i < 2:
                        a, b = keys[i][0], keys[i][1]
                    else:
                        a, b = keys[i - 1][0] * keys[i - 2][0], keys[i - 1][0] + keys[i - 2][0]  # generate new keys
                        keys.append((a, b))
                    encrypted += alph[(alph_rev[s] * a + b) % len(alph)]  # формула

            except KeyError:
                dialog = WarnDialog("Ошибка", f"Символ <{s}> отсутсвует в заданном алфавите.")
                dialog.exec_()
                return ""
            return encrypted
        else:
            dialog = WarnDialog("Ошибка", "Числа a1, a2 и m должны быть взаимно простыми")
            dialog.exec_()
            return ''
