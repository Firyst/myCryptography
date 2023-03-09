import numpy as np

interactive = False
plain_text = "VERY SECRET INFORM"
cipher_text ="KBTYJHMIWGCFCJMQOJ"
alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
alph_rev = dict(zip(alph, range(len(alph))))  # reversed alphabet
block = 3


def invmod2(pt_matrix, ct_matrix):
    assert np.ndim(pt_matrix) == 2
    assert pt_matrix.shape[0] == pt_matrix.shape[1]
    n = pt_matrix.shape[0]
    matrix = np.hstack((pt_matrix, ct_matrix))

    # Приводим матрицу А к диагональному виду
    for nrow, row in enumerate(matrix):
        # nrow равен номеру строки
        # row содержит саму строку матрицы
        divider = row[nrow]  # диагональный элемент
        # делим на диагональный элемент.
        row *= pow(int(divider) % len(alph), -1, len(alph))
        row %= len(alph)
        # теперь надо вычесть приведённую строку из всех нижележащих строчек
        for lower_row in matrix[nrow + 1:]:
            factor = lower_row[nrow]  # элемент строки в колонке nrow
            lower_row -= factor*row  # вычитаем, чтобы получить ноль в колонке nrow
    matrix = matrix % len(alph)
    # обратный ход
    for nrow in range(len(matrix) - 1, 0, -1):
        row = matrix[nrow]
        for upper_row in matrix[:nrow]:
            factor = upper_row[nrow]
            # Вычитание целой строки на 15% быстрее, чем вычитание только правой части
            upper_row -= factor*row
    matrix %= len(alph)
    return matrix[:, n:].copy()


def to_text(matrix):
    res = ""
    for elem in matrix.reshape(1, block * block)[0]:
        res += alph[elem]
    return res


def to_matrix(text, size):
    coded = list()
    for s in text:
        coded.append(alph_rev[s])
    return np.array(coded).reshape(size, size).transpose()


def to_vector(text, size):
    return to_matrix(text, size).reshape(1, size ** 2).transpose()


def solution_matrix(input_matrix, size):
    matrix = np.zeros((size ** 2, size ** 2))

    for i in range(size):
        for j in range(size):
            for mv in range(0, size):
                mv2 = mv * size
                matrix[i + mv2, j + mv2] = input_matrix[j, i]
    # matrix = matrix.transpose()
    return matrix


if interactive:
    block_size = int(input("Введите размер блока: "))
    plain_text = input("Введите известный открытый текст: ")
    cipher_text = input("Введите соответствующий шифртекст: ")


# error check
if len(plain_text) != len(cipher_text):
    print("Длина введенного открытого текста и шифртекста не совпадает.")
    exit(1)

if len(plain_text) % (block ** 2):
    print("Длина текста не кратна квадрату длины блока.")
    exit(1)

blocks = len(plain_text) // (block ** 2)

for block_id in range(blocks):
    # convert to matrices
    plain_text_block = plain_text[block_id * (block ** 2):(block_id + 1) * (block ** 2)]
    cipher_text_block = cipher_text[block_id * (block ** 2):(block_id + 1) * (block ** 2)]
    plain_matrix = to_matrix(plain_text_block, block).astype(np.float64).transpose()
    cipher_matrix = to_matrix(cipher_text_block, block).astype(np.float64).transpose()

    print(f"Попытка восстановить ключ ({block_id + 1}/{blocks})")

    try:
        key = (invmod2(plain_matrix, cipher_matrix).transpose().astype(np.int32))
        print(f"Найденный ключ ({block_id + 1}):")
        print(to_text(key))
        print(str(key))
    except ValueError:
        print("Не удалось восстановить ключ")