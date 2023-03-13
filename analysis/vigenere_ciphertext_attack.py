from cryptos import vigenere

print("Взлом шифра с самоключом по шифртексту")
INPUT_TEXT = input("Введите шифртекст: ")
ALPH = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "

for i in range(1,int(input("Максимальная длина ключа: "))):
    print(f"ДЛИНА={str(i).ljust(8, ' ')}{vigenere.decrypt(INPUT_TEXT, ALPH, ALPH[0] * i + INPUT_TEXT, 2, False)}")
