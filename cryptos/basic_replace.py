from main import ProgramWindow
from json import load
from dialogs import WarnDialog
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
MODULE_NAME = "Простая замена"
PUNC = ' !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'


class Crypto(QWidget):
    def __init__(self, parent: ProgramWindow, page):
        super().__init__()
        uic.loadUi('resources/basic_replace.ui', self)
        self.parent_window = parent
        self.page = page
        print("init module basic replace")

        # self.auto_button.clicked.connect(self.auto_alph)
        self.move_left_button.clicked.connect(self.move_left)
        self.move_right_button.clicked.connect(self.move_right)

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
        self.alph1.setText(alph)
        self.alphabet_sel.setCurrentIndex(0)

    def move_left(self):
        text = self.alph1.text()
        if text:
            self.alph1.setText(text[1:] + text[0])

    def move_right(self):
        text = self.alph1.text()
        if text:
            self.alph1.setText(text[-1] + text[:-1])

    def encrypt(self):
        ignore_punc = self.parent_window.punctuation.isChecked()
        alph0, alph1 = self.alph0.text(), self.alph1.text()
        if len(alph0) == len(alph1):
            encrypted = ""
            replaces = dict(zip(alph0, alph1))
            s = "?"
            try:
                for s in self.parent_window.open_text():
                    if ignore_punc and s in PUNC:
                        # check if is punctuation
                        encrypted += s
                    else:
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
        ignore_punc = self.parent_window.punctuation.isChecked()
        alph1, alph0 = self.alph0.text(), self.alph1.text()
        if len(alph0) == len(alph1):
            decrypted = ""
            replaces = dict(zip(alph0, alph1))
            s = "?"
            try:
                for s in self.parent_window.cipher_text():
                    if ignore_punc and s in PUNC:
                        # check if is punctuation
                        decrypted += s
                    else:
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
