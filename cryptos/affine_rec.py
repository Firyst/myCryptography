from main import ProgramWindow
import math
from json import load
from dialogs import WarnDialog
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
MODULE_NAME = "Аффинный рек."
PUNC = ' !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

class Crypto(QWidget):
    def __init__(self, parent: ProgramWindow, page):
        super().__init__()
        uic.loadUi('resources/affine_rec.ui', self)
        self.parent_window = parent
        self.page = page
        print("init module affine recursive")

        # load alphabets.
        self.alphabet_sel.addItem("Выбрать")
        self.alphabet_sel.addItem("Авто")
        self.alphabet_sel.currentIndexChanged.connect(self.load_alphabet)
        with open("resources/alphabets.json", encoding="utf8") as f:
            for alph_name in load(f).keys():
                self.alphabet_sel.addItem(alph_name)

    def load_alphabet(self):
        """ Load alphabet from ./resources/alphabets.json """
        if self.alphabet_sel.currentIndex() == 0:
            return
        if self.alphabet_sel.currentIndex() == 1:
            # automatic alphabet
            alph = ''.join(sorted(list(set(self.parent_window.open_text()))))
        else:
            with open("resources/alphabets.json", encoding="utf8") as f:
                alph = load(f)[self.alphabet_sel.currentText()]

        self.alph0.setText(alph)
        self.alphabet_sel.setCurrentIndex(0)

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
        ignore_punc = self.parent_window.punctuation.isChecked()
        alph = list(self.alph0.text())
        alph_rev = dict(zip(alph, range(len(alph))))  # reversed alphabet
        try:
            # load keys
            a1, b1 = int(self.key_a1.value()), int(self.key_b1.value())
            a2, b2 = int(self.key_a2.value()), int(self.key_b2.value())
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
                i = 0
                for s in self.parent_window.cipher_text():
                    if ignore_punc and s in PUNC:
                        # detect punctuation
                        decrypted += s
                        continue

                    if i < 2:
                        a, b = keys[i][0], keys[i][1]
                    else:
                        a, b = (keys[i - 1][0] * keys[i - 2][0]) % len(alph), \
                            (keys[i - 1][1] + keys[i - 2][1]) % len(alph)  # generate new keys
                        keys.append((a, b))
                    ia = pow(a, -1, len(alph))  # inverted by module
                    decrypted += alph[((alph_rev[s] - b) * ia) % len(alph)]  # cipher formula
                    print(f"x=({alph_rev[s]}-{b})×{ia}={((alph_rev[s] - b) * ia) % len(alph)} mod 26")
                    i += 1

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
        ignore_punc = self.parent_window.punctuation.isChecked()
        alph = list(self.alph0.text())
        alph_rev = dict(zip(alph, range(len(alph))))  # reversed alphabet
        try:
            # load keys
            a1, b1 = int(self.key_a1.value()), int(self.key_b1.value())
            a2, b2 = int(self.key_a2.value()), int(self.key_b2.value())
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
                i = 0
                for s in self.parent_window.open_text():
                    if ignore_punc and s in PUNC:
                        # detect punctuation
                        encrypted += s
                        continue
                    print(s, i)
                    if i < 2:
                        a, b = keys[i][0], keys[i][1]
                    else:
                        a, b = (keys[i - 1][0] * keys[i - 2][0]) % 26, \
                            (keys[i - 1][1] + keys[i - 2][1]) % 26  # generate new keys
                        keys.append((a, b))

                    encrypted += alph[(alph_rev[s] * a + b) % len(alph)]  # формула
                    i += 1

            except KeyError:
                dialog = WarnDialog("Ошибка", f"Символ <{s}> отсутсвует в заданном алфавите.")
                dialog.exec_()
                return ""
            return encrypted
        else:
            dialog = WarnDialog("Ошибка", "Числа a1, a2 и m должны быть взаимно простыми")
            dialog.exec_()
            return ''
