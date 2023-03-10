from string import punctuation

INPUT_TEXT = ""

for s in punctuation + " \n":
    INPUT_TEXT = INPUT_TEXT.replace(s, "")
del s

if not INPUT_TEXT:
    INPUT_TEXT = input("Введите шифртекст: ")

print("Рассчет индексов совпадений...")


def check_language_by_ioc(value):
    if len(INPUT_TEXT) > 999:
        iocs = {"EN": 0.0644, "RU": 0.0553}  # defaults
    else:
        iocs = {"!": 0.05, "!": 0.06}  # defaults

    res = ""
    minim = 9999
    for cur in iocs:
        if abs(value - iocs[cur]) < 0.01 and abs(value - iocs[cur]) < minim:
            res = cur
            minim = iocs[cur]
    return res


def calculate_coindence(text):
    # посчитать количество совпадений
    coincidence = dict()
    for s in text:
        coincidence[s] = coincidence.get(s, 0) + 1
    # рассчитать значение ИС
    ioc = 0
    for s in coincidence.keys():
        ioc += (coincidence[s] * (coincidence[s] - 1))
    return ioc / (len(text) * max(1, len(text) - 1))


values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
for key_len in range(2, 20):
    total_ioc = 0
    for i in range(key_len):
        total_ioc += calculate_coindence(INPUT_TEXT[i::key_len])
    values[key_len - 2] = total_ioc / key_len


print('Длин\t' + "\t\t".join(map(str, range(2, 20))))
print('Знач\t' + "".join(map(lambda x: str(round(x, 4)).ljust(8, " "), values)))
print('\t\t' + "\t\t".join(map(check_language_by_ioc, values)))
