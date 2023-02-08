from main import ProgramWindow
import math
from json import load
from dialogs import WarnDialog
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
MODULE_NAME = "Аффинный"
PUNC = ' !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'


class Crypto(QWidget):
    def __init__(self, parent: ProgramWindow, page):
        super().__init__()
        uic.loadUi('resources/affine.ui', self)
        self.parent_window = parent
        self.page = page
        print("init module affine")

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
        alph = list(self.alph0.text())
        alph_rev = dict(zip(alph, range(len(alph))))  # reversed alphabet
        ignore_punc = self.parent_window.punctuation.isChecked()

        try:
            # load keys
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
                    if ignore_punc and s in PUNC:
                        # detect punctuation
                        decrypted += s
                        continue
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

    def encrypt(self) -> str:
        alph = list(self.alph0.text())
        alph_rev = dict(zip(alph, range(len(alph))))  # создать обратный словарь для более быстрой работы
        ignore_punc = self.parent_window.punctuation.isChecked()

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
                    if ignore_punc and s in PUNC:
                        # detect punctuation
                        encrypted += s
                        continue

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
