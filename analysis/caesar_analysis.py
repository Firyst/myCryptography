import enchant
from cryptos.basic_replace import decrypt

d = enchant.Dict("en_US")

alphabet = "abcdefghijklmnopqrstuvwxyz .,"
text = "SBDROLKDNKRRUE".lower()
variants = []  # possible (variant score, string)


new_alphabet = alphabet
for i in range(len(alphabet)):
    new_alphabet = new_alphabet[1:] + new_alphabet[0]
    new_text = decrypt(text, alphabet, new_alphabet, False)
    score = 0
    for word in new_text.split():
        if d.check(word):
            score += 1

    if score > 0:
        variants.append((score, new_text))


variants.sort(key=lambda i: i[0], reverse=True)

for i, var in enumerate(variants):
    print(f"Variant {i + 1} (words={var[0]}: {var[1]}")
