from cryptos import vigenere
import vigenere_opentext

INPUT_TEXT = ""
ALPH = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "

if not INPUT_TEXT:
    INPUT_TEXT = input("Введите шифртекст: ")

print("Атака на шифр Виженера с самолючом по открытому тексту")
last_word = ""
while 1:
    if not last_word:
        print("Введите слово, которое может быть зашифровано в исходном тексте")
    else:
        print("Введите слово или номер сдвига для полного восстановления:")
    word = input("Ввод: ")

    try:
        # проверка, было ли введено значение
        mv = int(word)
        max_key_len = int(input("Укажите максимальную длину ключа: "))
        for k in range(1, max_key_len):
            print(f"ДЛИНА={str(k).ljust(8, ' ')}{vigenere_opentext.opentext_key_attack(INPUT_TEXT, last_word, mv, k, ALPH)}")
        continue

    except ValueError:
        pass

    if word == "":
        break

    for i in range(len(INPUT_TEXT) - len(word)):
        key = word.rjust(len(word) + i, ALPH[0]).ljust(len(INPUT_TEXT), ALPH[0])
        # print(key)
        decrypted = vigenere.decrypt(INPUT_TEXT, ALPH, key, 1, False)
        print(f"СДВИГ={str(i).ljust(8, ' ')}{decrypted}   [{decrypted[i:len(word)+i]}]")

    last_word = word
