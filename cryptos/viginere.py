from main import ProgramWindow
from json import load
from dialogs import WarnDialog
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
import random
MODULE_NAME = "Шифр Виженера"
SUPPORTS_PUNC = 1
PUNC = ' !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'


def encrypt(message, alph, key, method, ignore_punc: bool):
    """
    method: 0=simple gamma, 1=use open text, 2=use cipher text
    """
    encrypted = ""
    alph_rev = dict(zip(alph, range(len(alph))))  # reversed alphabet

    if method == 1:
        key += message  # generate open text key
    i = 0
    for s in message:
        if ignore_punc and s in PUNC:
            # check if is punctuation
            encrypted += s
        else:
            if method <= 1:
                encrypted += alph[(alph_rev[s] + alph_rev[key[i]]) % len(alph)]
                print(s, alph_rev[s], alph_rev[key[i]], (alph_rev[s] + alph_rev[key[i]]) % len(alph))
                i += 1
            elif method == 2:
                if i < len(key):
                    # still using key
                    encrypted += alph[(alph_rev[s] + alph_rev[key[i]]) % len(alph)]
                else:
                    # use ciphertext symbols
                    encrypted += alph[(alph_rev[s] + alph_rev[encrypted[i - len(key)]]) % len(alph)]
                i += 1
    return encrypted


def decrypt(message, alph, key, method, ignore_punc: bool):
    """
    method: 0=simple gamma, 1=use open text, 2=use cipher text
    """
    decrypted = ""
    alph_rev = dict(zip(alph, range(len(alph))))  # reversed alphabet

    if method == 2:
        key += message  # generate cipher text key

    i = 0
    for s in message:
        if ignore_punc and s in PUNC:
            # check if is punctuation
            decrypted += s
        else:
            if method == 0 or method == 2:
                decrypted += alph[(alph_rev[s] - alph_rev[key[i]]) % len(alph)]
                i += 1
            elif method == 1:
                if i < len(key):
                    # still using key
                    decrypted += alph[(alph_rev[s] - alph_rev[key[i]]) % len(alph)]
                else:
                    # use open text symbols
                    decrypted += alph[(alph_rev[s] - alph_rev[decrypted[i - len(key)]]) % len(alph)]
                i += 1
    return decrypted


class Crypto(QWidget):
    def __init__(self, parent: ProgramWindow, page):
        super().__init__()
        uic.loadUi('resources/viginere.ui', self)
        self.SUPPORTS_PUNC = SUPPORTS_PUNC
        self.parent_window = parent
        self.page = page
        print("init module Viginere")

        # Bind button
        self.key_generate.clicked.connect(self.generate_random_key)

        self.key_input.textChanged.connect(self.key_size_changed)

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

    def key_size_changed(self):
        current_key_size = len(self.key_input.text())
        if current_key_size:
            self.key_len.setValue(current_key_size)

    def get_key_method(self, msg_len: int):
        key = self.key_input.text()
        method = self.key_select.currentIndex()
        if not key:
            dialog = WarnDialog("Ошибка", f"Ключ не задан")
            dialog.exec_()
            return ""
        if method == 0:
            key *= (msg_len // len(key) + 1)
        return key, method

    def generate_random_key(self):
        alph = self.alph0.text()

        if not alph:
            dialog = WarnDialog("Ошибка", f"Алфавит не задан")
            dialog.exec_()
            return

        key = ""
        for i in range(self.key_len.value()):
            key += alph[random.randint(0, len(alph) - 1)]
        self.key_input.setText(key)

    def encrypt(self):
        ignore_punc = self.parent_window.punctuation.isChecked()
        alph = self.alph0.text()
        key, method = self.get_key_method(len(self.parent_window.open_text()))
        try:
            return encrypt(self.parent_window.open_text(), alph, key, method, ignore_punc)
        except KeyError:
            dialog = WarnDialog("Ошибка", f"Символ отсутсвует в заданном алфавите.")
            dialog.exec_()
            return ""
        except ValueError:
            pass

    def decrypt(self):
        ignore_punc = self.parent_window.punctuation.isChecked()
        alph = self.alph0.text()
        key, method = self.get_key_method(len(self.parent_window.cipher_text()))
        try:
            return decrypt(self.parent_window.cipher_text(), alph, key, method, ignore_punc)
        except KeyError:
            dialog = WarnDialog("Ошибка", f"Символ отсутсвует в заданном алфавите.")
            dialog.exec_()
            return ""
        except ValueError:
            pass
