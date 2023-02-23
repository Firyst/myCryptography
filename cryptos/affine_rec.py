from main import ProgramWindow
import math
from json import load
from dialogs import WarnDialog
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
MODULE_NAME = "Аффинный рек."
SUPPORTS_PUNC = 1
PUNC = ' !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'


def decrypt(message, alph, ignore_punc: bool, a1: int, b1: int, a2: int, b2: int) -> str:
    """Decrypt function, will be called automatically"""
    alph_rev = dict(zip(alph, range(len(alph))))  # reversed alphabet
    decrypted = ""
    s = "?"
    a1, a2 = pow(a1, -1, len(alph)), pow(a2, -1, len(alph))  # calculate inverted keys
    keys = [(a1, b1), (a2, b2)]
    i = 0
    for s in message:
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
        decrypted += alph[((alph_rev[s] - b) * a) % len(alph)]  # cipher formula
        i += 1

    return decrypted


def encrypt(message, alph, ignore_punc: bool, a1: int, b1: int, a2: int, b2: int) -> str:
    alph_rev = dict(zip(alph, range(len(alph))))  # reversed alphabet
    encrypted = ""
    s = "?"
    keys = [(a1, b1), (a2, b2)]
    i = 0
    for s in message:
        if ignore_punc and s in PUNC:
            # detect punctuation
            encrypted += s
            continue
        if i < 2:
            a, b = keys[i][0], keys[i][1]
        else:
            a, b = (keys[i - 1][0] * keys[i - 2][0]) % len(alph), \
                   (keys[i - 1][1] + keys[i - 2][1]) % len(alph)  # generate new keys
            keys.append((a, b))

        encrypted += alph[(alph_rev[s] * a + b) % len(alph)]  # формула
        i += 1

    return encrypted


class Crypto(QWidget):
    def __init__(self, parent: ProgramWindow, page):
        super().__init__()
        uic.loadUi('resources/affine_rec.ui', self)
        self.SUPPORTS_PUNC = SUPPORTS_PUNC
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

    def decrypt(self):
        alph = list(self.alph0.text())
        ignore_punc = self.parent_window.punctuation.isChecked()

        try:
            # load keys
            a1, b1 = int(self.key_a1.value()), int(self.key_b1.value())
            a2, b2 = int(self.key_a2.value()), int(self.key_b2.value())
        except ValueError:
            dialog = WarnDialog("Ошибка", "Ключи заданы неверно")
            dialog.exec_()
            return ''
        if math.gcd(len(alph), a1) and math.gcd(len(alph), a2) == 1:
            try:
                return decrypt(self.parent_window.cipher_text(), alph, ignore_punc, a1, b1, a2, b2)
            except KeyError:
                dialog = WarnDialog("Ошибка", f"Символ отсутсвует в заданном алфавите.")
                dialog.exec_()
                return ""
        else:
            dialog = WarnDialog("Ошибка", "Числа a1, a2 и m должны быть взаимно простыми")
            dialog.exec_()
            return ''

    def encrypt(self) -> str:
        alph = list(self.alph0.text())
        ignore_punc = self.parent_window.punctuation.isChecked()

        try:
            # load keys
            a1, b1 = int(self.key_a1.value()), int(self.key_b1.value())
            a2, b2 = int(self.key_a2.value()), int(self.key_b2.value())
        except ValueError:
            dialog = WarnDialog("Ошибка", "Ключи заданы неверно")
            dialog.exec_()
            return ''
        if math.gcd(len(alph), a1) and math.gcd(len(alph), a2) == 1:
            try:
                return encrypt(self.parent_window.open_text(), alph, ignore_punc, a1, b1, a2, b2)
            except KeyError:
                dialog = WarnDialog("Ошибка", f"Символ отсутсвует в заданном алфавите.")
                dialog.exec_()
                return ""
        else:
            dialog = WarnDialog("Ошибка", "Числа a1, a2 и m должны быть взаимно простыми")
            dialog.exec_()
            return ''
