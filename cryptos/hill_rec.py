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

MODULE_NAME = "Шифр Хилла (рек.)"
SUPPORTS_PUNC = 0
PUNC = ' !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

sys.setrecursionlimit(2 ** 16)


class InvalidKeyException(Exception):
    pass


def encrypt(message, alph, ignore_punc: bool, key1, key2, block_size: int) -> str:
    print("ENCRYPT")
    alph_rev = dict(zip(alph, range(len(alph))))  # reversed alphabet
    encrypted = ""

    key1 = np.array(key1)
    key1 = key1.reshape((block_size, block_size))

    key2 = np.array(key2)
    key2 = key2.reshape((block_size, block_size))

    det1 = round(np.linalg.det(key1))
    det2 = round(np.linalg.det(key2))
    if det1 == 0 or det2 == 0:
        raise ArithmeticError("определитель равен нулю :(")

    if math.gcd(int(det1), len(alph)) != 1 or math.gcd(int(det2), len(alph)) != 1:
        raise InvalidKeyException

    coded = []  # encoded message by indexes
    for s in message:
        if ignore_punc and s in PUNC:
            # detect punctuation
            continue
        coded.append(alph_rev[s])

    extend_symbol = 0
    if " " in alph:
        extend_symbol = alph.index(" ")  # если есть пробел, то используем его как пустышку
    while len(coded) % block_size != 0:
        coded.append(extend_symbol)  # fill until fits block size

    last_key1 = key1
    last_key2 = key2

    for block_id in range(len(coded) // block_size):
        text_block = np.full((block_size, 1), 0)  # create new vector
        for sym_i in range(block_size):
            text_block[sym_i, 0] = coded[block_id * block_size + sym_i]  # create text block vector

        # keys
        if block_id == 0:
            key = last_key1
        elif block_id == 1:
            key = last_key2
        else:
            key = np.dot(last_key2, last_key1) % len(alph)
            last_key1, last_key2 = last_key2, key

        encrypted_block = np.dot(key, text_block)
        print("BLOCK", block_id, '\n', key, '\n', text_block, '\n', encrypted_block % len(alph))

        for sym_i in range(block_size):
            encrypted += alph[encrypted_block[sym_i, 0] % len(alph)]  # convert into text

    return encrypted


def decrypt(message, alph, ignore_punc: bool, key1, key2, block_size: int) -> str:
    # поиск обратной матрицы по модулю.
    print("DECRYPT")
    def matrix_invmod(input_matrix, mod):  # Finds the inverse of matrix A by mod p
        def minor(matrix, i, j):  # caclulate minor
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

    key1 = np.array(key1)
    key1 = key1.reshape((block_size, block_size))

    key2 = np.array(key2)
    key2 = key2.reshape((block_size, block_size))

    det1 = round(np.linalg.det(key1))
    det2 = round(np.linalg.det(key2))
    if det1 == 0 or det2 == 0:
        raise ArithmeticError("определитель равен нулю :(")

    if math.gcd(int(det1), len(alph)) != 1 or math.gcd(int(det2), len(alph)) != 1:
        raise InvalidKeyException

    key1 = matrix_invmod(key1, len(alph))  # calculate inverted matrix
    key2 = matrix_invmod(key2, len(alph))

    coded = []  # encoded message by indexes
    for s in message:
        if ignore_punc and s in PUNC:
            # detect punctuation
            continue
        coded.append(alph_rev[s])

    while len(coded) % block_size != 0:
        coded.append(0)  # fill until fits block size

    last_key1 = key1
    last_key2 = key2

    for block_id in range(len(coded) // block_size):
        text_block = np.full((block_size, 1), 0)  # create new vector
        for sym_i in range(block_size):
            text_block[sym_i, 0] = coded[block_id * block_size + sym_i]  # create text block vector

        # keys
        if block_id == 0:
            key = last_key1
        elif block_id == 1:
            key = last_key2
        else:
            key = np.dot(last_key1, last_key2) % len(alph)
            last_key1, last_key2 = last_key2, key
        decrypted_block = np.dot(key, text_block)
        print("BLOCK", block_id, '\n', key, '\n', text_block, '\n', decrypted_block % len(alph))
        for sym_i in range(block_size):
            decrypted += alph[int(decrypted_block[sym_i, 0]) % len(alph)]  # convert into text

    return decrypted


class Crypto(QWidget):
    def __init__(self, parent: ProgramWindow, page):
        super().__init__()
        uic.loadUi('resources/hill_rec.ui', self)
        self.SUPPORTS_PUNC = SUPPORTS_PUNC
        self.parent_window = parent
        self.page = page
        print("init module hill recursive")

        self.key1 = list()
        self.key2 = list()

        self.block_size.valueChanged.connect(self.set_matrix_size)
        self.matrix_view.cellChanged.connect(self.matrix_changed)
        self.matrix_view2.cellChanged.connect(self.matrix_changed)
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

        self.key_enter.setMaxLength(2 * (current_size ** 2))

        if alph:
            self.key_enter.setText(alph[0] * (2 * current_size ** 2))

        self.matrix_view.setRowCount(current_size)
        self.matrix_view.setColumnCount(current_size)
        self.matrix_view2.setRowCount(current_size)
        self.matrix_view2.setColumnCount(current_size)
        self.matrix_view.resizeColumnsToContents()
        self.matrix_view2.resizeColumnsToContents()
        for iy in range(current_size):
            for ix in range(current_size):
                new_item = QTableWidgetItem("0")  # создаем элемент таблицы со значением
                new_item.setData(Qt.DisplayRole, 0)
                self.matrix_view.setItem(iy, ix, new_item)

                new_item = QTableWidgetItem("0")  # создаем элемент таблицы со значением
                new_item.setData(Qt.DisplayRole, 0)
                self.matrix_view2.setItem(iy, ix, new_item)

    # key updates

    def generate_random_key(self):
        current_size = self.block_size.value()
        alph = self.alph0.text()

        if not alph:
            dialog = WarnDialog("Ошибка", f"Алфавит не задан")
            dialog.exec_()
            return

        key1 = np.random.random_integers(0, len(alph), (current_size, current_size))
        key2 = np.random.random_integers(0, len(alph), (current_size, current_size))
        det1 = round(np.linalg.det(key1))
        det2 = round(np.linalg.det(key2))
        try:
            if (det1 == 0) or (math.gcd(int(det1), len(alph)) != 1):
                self.generate_random_key()
                return
            if (det2 == 0) or (math.gcd(int(det2), len(alph)) != 1):
                self.generate_random_key()
                return
        except RecursionError:
            dialog = WarnDialog("Ошибка", f"Не удалось сгенерировать ключ с выбранными параметрами")
            dialog.exec_()
            return
        # set key
        self.matrix_view.blockSignals(1)
        self.matrix_view2.blockSignals(1)
        for iy in range(current_size):
            for ix in range(current_size):
                self.matrix_view.setItem(iy, ix, QTableWidgetItem(str(key1[ix, iy])))
                self.matrix_view2.setItem(iy, ix, QTableWidgetItem(str(key2[ix, iy])))

        self.matrix_view.blockSignals(0)
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
            key1 = []
            key2 = []
            text_key1 = ""
            text_key2 = ""
            current_size = self.block_size.value()

            for iy in range(current_size):
                for ix in range(current_size):
                    try:
                        key1.append(int(self.matrix_view.item(iy, ix).text()))
                        key2.append(int(self.matrix_view2.item(iy, ix).text()))
                        if len(alph) > 1:
                            text_key1 += alph[int(self.matrix_view.item(iy, ix).text()) % len(alph)]
                            text_key2 += alph[int(self.matrix_view2.item(iy, ix).text()) % len(alph)]
                    except AttributeError:
                        # matrix is not filled...
                        return
                    except ValueError:
                        dialog = WarnDialog("Ошибка", f"Введено некорректное значение")
                        dialog.exec_()
                        self.matrix_view.setItem(iy, ix, QTableWidgetItem("0"))
                        self.matrix_view2.setItem(ix, iy, QTableWidgetItem("0"))
                        return
            if key1 != self.key1 or key2 != self.key2:
                self.key_enter.blockSignals(1)
                self.key_enter.setText(text_key1 + text_key2)
                self.key1 = key1
                self.key2 = key2
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

            while len(key) < 2 * (self.block_size.value() ** 2):
                key.append(0)

            # fill up the matrix
            self.matrix_view.blockSignals(1)
            self.matrix_view2.blockSignals(2)

            # key 1
            for i, s in enumerate(key[:len(key) // 2]):
                self.matrix_view.setItem(i // self.block_size.value(),
                                         i % self.block_size.value(),
                                         QTableWidgetItem(str(s)))
            # key 2
            for i, s in enumerate(key[len(key) // 2:]):
                self.matrix_view2.setItem(i // self.block_size.value(),
                                          i % self.block_size.value(),
                                          QTableWidgetItem(str(s)))
            self.matrix_view.blockSignals(0)
            self.matrix_view2.blockSignals(0)
            if key:
                self.key1 = key[:len(key) // 2]
                self.key2 = key[len(key) // 2:]

    def decrypt(self):
        alph = list(self.alph0.text())
        ignore_punc = self.parent_window.punctuation.isChecked()
        try:
            return decrypt(self.parent_window.cipher_text(), alph, ignore_punc, self.key1, self.key2,
                           self.block_size.value())
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
        ignore_punc = self.parent_window.punctuation.isChecked()
        try:
            return encrypt(self.parent_window.open_text(), alph, ignore_punc, self.key1, self.key2,
                           self.block_size.value())
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
