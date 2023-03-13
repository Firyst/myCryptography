from cryptos.vigenere import decrypt

default_ru = " ОАЕИНТСЛВРМКУДПЯЬБГЗЫЧШЙЖЮХЦЩЭФЪЁ"

with open("data/message1.txt", encoding="utf8") as f:
    INPUT_TEXT = f.read()

ALPH = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ "
KEY_LEN = int(input("Длина ключа: "))


def scan_text(text):
    res = dict()
    for s in text:
        res[s] = res.get(s, 0) + 1
    return res


key = ""
for i in range(KEY_LEN):
    stats = sorted(list(scan_text(INPUT_TEXT[i::KEY_LEN]).items()), key=lambda x: x[1], reverse=True)
    # print(stats)
    key += ALPH[(ALPH.find(stats[0][0]) - ALPH.find(" ")) % len(ALPH)]
print("Найденный ключ", key)
print("Текст:")
print(decrypt(INPUT_TEXT, ALPH, key * 1000, 0, False))
