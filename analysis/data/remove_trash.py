from string import punctuation

a = """Шифр Хилла представляет собой пример блочного шифра, основанного на матричных преобразованиях с использованием арифметики остатков. Данный шифр устроен следующим образом.
Открытый текст рассматривается как последовательность символов некоторого алфавита мощностью  которые представляются элементами множества  Перед зашифрованием открытый текст разбивается на блоки длиной, и каждый блок представляется в виде -мерного вектора.
"""

for e in punctuation + " ":
    a = a.replace(e, '')
print(a.replace("\n", "").upper())