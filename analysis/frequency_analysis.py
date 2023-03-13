from string import punctuation, digits, ascii_lowercase
import math

WHITELIST = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ "


def filter_text(text, whitelist=WHITELIST):
    res = ""
    for s in text:
        if s in whitelist:
            res += s
    return res


def scan_text(text, whitelist=WHITELIST):
    res = dict()
    for s in text:
        if s in whitelist:
            res[s] = res.get(s, 0) + 1
    return res


SCAN_FILE = "data/russian1.txt"
MSG_FILE = "data/message1.txt"



with open(SCAN_FILE, "r", encoding="utf8") as f:
    # default_data = scan_text(f.read().upper())
    bruh = f.read().upper()

with open(MSG_FILE, "r", encoding="utf8") as f:
    crypto_text = f.read().upper()
    crypto_data = scan_text(crypto_text)

with open(MSG_FILE, "w", encoding="utf8") as f:
    f.write(filter_text(bruh))

replaces = dict()
freq1 = sorted(list(default_data.items()), key=lambda x: x[1], reverse=True)
freq2 = sorted(list(crypto_data.items()), key=lambda x: x[1], reverse=True)


for i in range(len(crypto_data)):
    replaces[freq2[i][0]] = freq1[i][0]

print(replaces)
print("Common: " + ''.join(replaces.values()))
print("Crypto: " + ''.join(replaces.keys()))

# write some rules here
replaces["Я"] ="К"
# now decrypt text
decrypted = ""
for s in crypto_text:
    decrypted += replaces[s]

print(decrypted)