import enchant
from math import gcd
from cryptos.affine import decrypt

d = enchant.Dict("en_US")

alphabet = " abcdefghijklmnopqrstuvwxyz"
text = "mgccifnkfqpgzingfloktjiboqtmkftoiboqn"
variants = []  # possible (variant score, string, keys)


new_alphabet = alphabet

for a in range(len(alphabet)):
    for b in range(len(alphabet)):
        if gcd(a, len(alphabet)) != 1:  # check if a key is correct
            continue
        new_text = decrypt(text, alphabet, False, a, b)
        score = 0
        for word in new_text.split():
            if d.check(word):
                score += 1

        if score > 0:
            variants.append((score, new_text, (a, b)))


variants.sort(key=lambda i: i[0], reverse=True)

for i, var in enumerate(variants[:16]):
    print(f"Variant {i + 1} (words={var[0]}; keys={var[2]}: {var[1]}")
