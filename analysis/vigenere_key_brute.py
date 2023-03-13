import enchant
from cryptos.vigenere import decrypt
from itertools import product
from time import time

d = enchant.Dict("en_US")

alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ .,"
print("Перебор ключей")
variants = []  # possible (variant score, string, keys)

text = input("Введите шифртекст: ")
mode = input("Тип гаммы (0=повт, 1=откр): ")
key_len = int(input("Длина ключа: "))

new_alphabet = alphabet

mult = len(text) // key_len + 1

for comb in product(alphabet, repeat=key_len):
    start = time()
    key = ''.join(comb)*mult
    # print("gen key ", time() - start)
    new_text = decrypt(text, alphabet, key, 0, 0)

    score = 0


    for word in new_text.split():
        if d.check(word):
            score += 1

    if score > 0:
        variants.append((score, new_text, ''.join(comb)))



variants.sort(key=lambda i: i[0], reverse=True)

for i, var in enumerate(variants[:16]):
    print(f"Вариант {i + 1} (words={var[0]}; keys={var[2]}: {var[1]}")
