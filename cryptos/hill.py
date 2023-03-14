import numpy.random
import sys
from main import ProgramWindow
import math
from json import load
from dialogs import WarnDialog
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
import numpy as np
MODULE_NAME = "Шифр Хилла"
SUPPORTS_PUNC = 0
PUNC = ' !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

sys.setrecursionlimit(2**16)


class InvalidKeyException(Exception):
    pass


def encrypt(message, alph, key, block_size: int) -> str:
    alph_rev = dict(zip(alph, range(len(alph))))  # reversed alphabet
    encrypted = ""

    key = np.array(key)
    key = key.reshape((block_size, block_size))

    det = round(np.linalg.det(key))
    if det == 0:
        raise ArithmeticError("определитель не равен нулю :(")

    if math.gcd(int(det), len(alph)) != 1:
        raise InvalidKeyException

    coded = []  # encoded message by indexes
    for s in message:
        coded.append(alph_rev[s])

    extend_symbol = 0
    if " " in alph:
        extend_symbol = alph.index(" ")  # если есть пробел, то используем его как пустышку
    while len(coded) % block_size != 0:
        coded.append(extend_symbol)  # fill until fits block size

    for block_id in range(len(coded) // block_size):
        text_block = np.full((block_size, 1), 0)  # create new vector
        for sym_i in range(block_size):
            text_block[sym_i, 0] = coded[block_id * block_size + sym_i]  # create text block vector
        encrypted_block = np.dot(key, text_block)
        print(block_id, text_block, encrypted_block % len(alph))
        for sym_i in range(block_size):
            encrypted += alph[encrypted_block[sym_i, 0] % len(alph)]  # convert into text

    return encrypted


def decrypt(message, alph, key, block_size: int) -> str:
    # поиск обратной матрицы по модулю.
    def matrix_invmod(input_matrix, mod):  # обратная по модулю
        def minor(matrix, i, j):  # расчет минора
            matrix = np.array(matrix)
            minor = np.zeros(shape=(len(matrix) - 1, len(matrix) - 1))
            p = 0
            for s in range(0, len(minor)):
                if p == i:
                    p = p + 1
                q = 0
                for t in range(0, len(minor)):
                    if q == j:
                        q = q + 1
                    minor[s][t] = matrix[p][q]
                    q = q + 1
                p = p + 1
            return minor

        n = len(input_matrix)
        input_matrix = np.matrix(input_matrix)
        adj = np.zeros(shape=(n, n))
        for i in range(0, n):
            for j in range(0, n):
                adj[i][j] = ((-1) ** (i + j) * int(round(np.linalg.det(minor(input_matrix, j, i))))) % mod
        return (pow(int(round(np.linalg.det(input_matrix))), -1, mod) * adj) % mod

    alph_rev = dict(zip(alph, range(len(alph))))  # reversed alphabet
    decrypted = ""

    key = np.array(key)
    key = key.reshape((block_size, block_size))

    det = round(np.linalg.det(key))
    if det == 0:
        raise ArithmeticError("определитель не равен нулю :(")

    if math.gcd(int(det), len(alph)) != 1:
        raise InvalidKeyException

    key = matrix_invmod(key, len(alph))  # calculate inverted matrix
    print(key)
    coded = []  # encoded message by indexes
    for s in message:
        coded.append(alph_rev[s])

    while len(coded) % block_size != 0:
        coded.append(0)  # fill until fits block size

    for block_id in range(len(coded) // block_size):
        text_block = np.full((block_size, 1), 0)  # create new vector
        for sym_i in range(block_size):
            text_block[sym_i, 0] = coded[block_id * block_size + sym_i]  # create text block vector
        decrypted_block = np.dot(key, text_block)

        for sym_i in range(block_size):
            decrypted += alph[int(decrypted_block[sym_i, 0]) % len(alph)]  # convert into text

    return decrypted


class Crypto(QWidget):
    def __init__(self, parent: ProgramWindow, page):
        super().__init__()
        uic.loadUi('resources/hill.ui', self)
        self.parent_window = parent
        self.page = page
        print("init module hill")

        self.SUPPORTS_PUNC = SUPPORTS_PUNC
        self.key = list()

        self.block_size.valueChanged.connect(self.set_matrix_size)
        self.matrix_view.cellChanged.connect(self.matrix_changed)
        self.key_enter.textChanged.connect(self.line_key_changed)
        self.key_enter.editingFinished.connect(self.matrix_changed)  # fill missing symbols
        self.alph0.textChanged.connect(self.alphabet_changed)
        self.button_generate_key.clicked.connect(self.generate_random_key)
        # load alphabets.
        self.alphabet_sel.addItem("Выбрать")
        self.alphabet_sel.addItem("Авто")
        self.alphabet_sel.currentIndexChanged.connect(self.load_alphabet)
        with open("resources/alphabets.json", encoding="utf8") as f:
            for alph_name in load(f).keys():
                self.alphabet_sel.addItem(alph_name)

        self.set_matrix_size()

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

    def alphabet_changed(self):
        if self.alph0.text():
            self.matrix_view.setEnabled(1)
            self.key_enter.setEnabled(1)
        else:
            self.matrix_view.setEnabled(0)
            self.key_enter.setEnabled(0)

    def set_matrix_size(self):
        current_size = self.block_size.value()
        alph = self.alph0.text()

        self.key_enter.setMaxLength(current_size ** 2)

        if alph:
            self.key_enter.setText(alph[0] * current_size ** 2)

        self.matrix_view.setRowCount(current_size)
        self.matrix_view.setColumnCount(current_size)
        self.matrix_view.resizeColumnsToContents()

        for iy in range(current_size):
            for ix in range(current_size):

                new_item = QTableWidgetItem("0")  # создаем элемент таблицы со значением
                new_item.setData(Qt.DisplayRole, 0)
                self.matrix_view.setItem(iy, ix, new_item)

    # key updates

    def generate_random_key(self):
        current_size = self.block_size.value()
        alph = self.alph0.text()

        if not alph:
            dialog = WarnDialog("Ошибка", f"Алфавит не задан")
            dialog.exec_()
            return

        key = np.random.random_integers(1, len(alph), (current_size, current_size))
        det = round(np.linalg.det(key))
        print(det)
        try:
            if (det == 0) or (math.gcd(int(det), len(alph)) != 1):
                self.generate_random_key()
                return
        except RecursionError:
            dialog = WarnDialog("Ошибка", f"Не удалось сгенерировать ключ с выбранными параметрами")
            dialog.exec_()
            return
        # set key
        self.matrix_view.blockSignals(1)
        for iy in range(current_size):
            for ix in range(current_size):
                new_item = QTableWidgetItem(str(key[ix, iy]))  # создаем элемент таблицы со значением
                self.matrix_view.setItem(iy, ix, new_item)

        self.matrix_view.blockSignals(0)
        self.matrix_changed()

    def matrix_changed(self):
        # key matrix was changed
        self.update_key(1)

    def line_key_changed(self):
        # field with string key was changed
        self.update_key(0)

    def update_key(self, source):
        alph = list(self.alph0.text())
        if source:
            # edited table
            key = []
            text_key = ""
            current_size = self.block_size.value()

            for iy in range(current_size):
                for ix in range(current_size):
                    try:
                        key.append(int(self.matrix_view.item(iy, ix).text()))
                        if len(alph) > 1:
                            text_key += alph[int(self.matrix_view.item(iy, ix).text()) % len(alph)]
                    except AttributeError:
                        # matrix is not filled...
                        return
                    except ValueError:
                        dialog = WarnDialog("Ошибка", f"Введено некорректное значение")
                        dialog.exec_()
                        new_item = QTableWidgetItem("0")  # создаем элемент таблицы со значением
                        self.matrix_view.setItem(iy, ix, new_item)
                        return
            if key != self.key:
                self.key_enter.blockSignals(1)
                self.key_enter.setText(text_key)
                self.key_enter.blockSignals(0)
        else:
            # edited line key
            key = []
            for s in self.key_enter.text():
                try:
                    symbol_index = alph.index(s)
                except ValueError:
                    dialog = WarnDialog("Ошибка", f"Символ отсутствует в заданном алфавите.")
                    dialog.exec_()
                    return
                key.append(symbol_index)

            while len(key) < self.block_size.value() ** 2:
                key.append(0)

            # fill up the matrix
            self.matrix_view.blockSignals(1)
            for i, s in enumerate(key):
                self.matrix_view.setItem(i // self.block_size.value(),
                                         i % self.block_size.value(),
                                         QTableWidgetItem(str(s)))
            self.matrix_view.blockSignals(0)
        if key and key != self.key:
            self.key = key

    def decrypt(self):
        alph = list(self.alph0.text())
        ignore_punc = self.parent_window.punctuation.isChecked()
        try:
            return decrypt(self.parent_window.cipher_text(), alph, self.key, self.block_size.value())
        except KeyError:
            dialog = WarnDialog("Ошибка", f"Символ отсутствует в заданном алфавите.")
            dialog.exec_()
            return ""
        except ArithmeticError:
            dialog = WarnDialog("Ошибка", f"Определитель матрицы-ключа равен 0.")
            dialog.exec_()
            return ""
        except InvalidKeyException:
            dialog = WarnDialog("Ошибка", f"Определитель матрицы-ключа должен быть взаимно прост с мощностью алфавита.")
            dialog.exec_()
            return ""

    def encrypt(self) -> str:
        alph = list(self.alph0.text())
        try:
            return encrypt(self.parent_window.open_text(), alph, self.key, self.block_size.value())
        except KeyError:
            dialog = WarnDialog("Ошибка", f"Символ отсутствует в заданном алфавите.")
            dialog.exec_()
            return ""
        except ArithmeticError:
            dialog = WarnDialog("Ошибка", f"Определитель матрицы-ключа равен 0.")
            dialog.exec_()
            return ""
        except InvalidKeyException:
            dialog = WarnDialog("Ошибка", f"Определитель матрицы-ключа должен быть взаимно прост с мощностью алфавита.")
            dialog.exec_()
            return ""

