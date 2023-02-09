from string import punctuation, digits, ascii_lowercase
import math

WHITELIST = ascii_lowercase + " "

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


SCAN_FILE = "data/english1.txt"
MSG_FILE = "data/message1.txt"

with open(SCAN_FILE, "r", encoding="utf8") as f:
    default_data = scan_text(f.read().lower())

with open(MSG_FILE, "r", encoding="utf8") as f:
    crypto_text = f.read().lower()
    crypto_data = scan_text(crypto_text)

with open(MSG_FILE, "w") as f:
    f.write(filter_text(crypto_text))

replaces = dict()
freq1 = sorted(list(default_data.items()), key=lambda x: x[1], reverse=True)
freq2 = sorted(list(crypto_data.items()), key=lambda x: x[1], reverse=True)


for i in range(len(crypto_data)):
    replaces[freq2[i][0]] = freq1[i][0]

print(replaces)
print("Common: " + ''.join(replaces.values()))
print("Crypto: " + ''.join(replaces.keys()))

# now decrypt text
decrypted = ""
for s in crypto_text:
    decrypted += replaces[s]

print(decrypted)