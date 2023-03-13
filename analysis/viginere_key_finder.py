# Метод Касиски

import math

INPUT_TEXT = ""

def divs(x):
    res = {x}
    for i in range(1, int(x ** 0.5) + 4):
        if x % i == 0:
            res.add(i)
    return res


def scan(text, length):
    scans = dict()  # word: set(distances)
    scanned_words = set()

    for word_i in range(len(text) - length + 1):
        word = text[word_i:word_i + length]
        if word in scanned_words:
            continue
        scanned_words.add(word)

        scans[word] = set()

        last_i = word_i
        for scan_i in range(len(text) - length + 1):
            scan_word = text[scan_i:scan_i + length]
            if scan_word == word and word_i != scan_i:
                scans[word].add(abs(scan_i - last_i))
                last_i = scan_i

        if len(scans[word]) <= 0:
            scans.pop(word)
    del scanned_words
    # print(scans)
    # определяем наиболее частый общий делитель
    res = dict()  # gcd: probability
    for word, dists in scans.items():
        if len(dists) > 1:
            counts = math.gcd(*dists)
        else:
            counts = dists.pop()
        for c in divs(counts):
            res[c] = res.get(c, 0) + 1
    res.pop(1)
    return res


print("Тест Касиски")
if not INPUT_TEXT:
    INPUT_TEXT = input("Введите шифртекст: ")
for search_len in range(2, 6):
    try:
        result = list(scan(INPUT_TEXT.lower(), search_len).items())
        result.sort(key=lambda x: x[1], reverse=True)
        total_count = sum([i[1] for i in result])
        print(f"Возможная длина ключа на повторах длины {search_len}:")
        for e in result[:5]:
            print("Длина", e[0], str(round((e[1] / total_count) * 100)) + "%")
    except KeyError:
        print("Не нашлось повторов длины", search_len)
