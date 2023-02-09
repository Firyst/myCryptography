import enchant
from math import gcd
from itertools import product
from cryptos.affine_rec import decrypt

d = enchant.Dict("en_US")

alphabet = " abcdefghijklmnopqrstuvwxyz"
text = "livfdsdznswnomxjzbpnktzjbswvcsjckdvgl"
variants = []  # possible (variant score, string, keys)


new_alphabet = alphabet

possible_a = []

for a in range(len(alphabet)):
    if gcd(a, len(alphabet)) == 1:
        possible_a.append(a)

print(f"Total combinations: {len(possible_a) ** 2 * len(alphabet) ** 2}")

for keys in product(possible_a, possible_a, range(len(alphabet)), range(len(alphabet))):
    a1, a2, b1, b2 = keys
    new_text = decrypt(text, alphabet, False, a1, b1, a2, b2)
    score = 0
    for word in new_text.split():
        if d.check(word) and (len(word) > 1 or word == "i"):
            score += 1

    if score > 0:
        variants.append((score, new_text, (a1, b1, a2, b2)))


variants.sort(key=lambda i: i[0], reverse=True)

for i, var in enumerate(variants[:16]):
    print(f"Variant {i + 1} (words={var[0]}: {var[1]}; keys={var[2]}")
