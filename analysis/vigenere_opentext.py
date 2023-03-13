# попытка подбора ключевого слова
from cryptos import vigenere


def repeated_key_length(cipher_text, known_text, known_pos, alph):
    """ Вычисление длины циклического ключа + подбор ключа """

    alph_rev = dict(zip(alph, range(len(alph))))

    for test_length in range(2, len(known_text)):
        key = ["\0"] * test_length  # create empty key

        for i in range(len(known_text)):
            pos = (known_pos + i) % test_length
            key_char = alph[(alph_rev[cipher_text[known_pos + i]] - alph_rev[known_text[i]]) % len(alph)]
            if key[pos] == "\0":
                # key not set
                key[pos] = key_char
            else:
                if key[pos] != key_char:
                    break
        else:
            return "".join(key)

    return -1


def opentext_key_attack(cipher_text, known_text, known_pos, key_length, alph):
    """ Атака по открытому тексту на шифр Виженера с самоключом по открытому тексту """
    alph_rev = dict(zip(alph, range(len(alph))))
    key = known_text.rjust(len(known_text) + known_pos, alph[0]).ljust(len(cipher_text) + len(known_text), alph[0])
    decrypted = vigenere.decrypt(cipher_text, alph, key, 1, False)
    key = list(key)

    pass_i = 1
    while 1:
        # print(''.join(key))
        try:
            for i in range(known_pos - key_length, len(known_text) + known_pos - key_length):
                key[i + key_length * (pass_i + 1)] = decrypted[i + key_length * pass_i]
                if i + key_length * (1 - pass_i) >= 0:
                    key[i + key_length * (1 - pass_i)] = alph[
                        (alph_rev[cipher_text[i + key_length * (-pass_i + 1)]] -
                         alph_rev[key[i + key_length * (-pass_i + 2)]]) % len(alph)]

        except IndexError:
            # all symbols decrypted
            break
        decrypted = vigenere.decrypt(cipher_text, alph, ''.join(key), 1, False)
        pass_i += 1

    return decrypted


if __name__ == "__main__":
    ALPH = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
    print("Атака по открытому тексту")
    text = input("Введите шифртекст: ")
    mode = input("Тип гаммы (0=повт, 1=откр): ")
    text_piece = input("Введите известный отрезок: ")
    text_pos = int(input("Введите позицию отрезка: "))
    # for possible_key_length in range(2, len(text) // 2):
    #     print(possible_key_length)
    #     opentext_key_attack(text, " МОЙ ", 30, possible_key_length,
    #                         "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ .,")

    if mode == "0":
        found_key = (repeated_key_length(text, text_piece, text_pos, ALPH))
        print("Найденный ключ:", found_key)
        print("Сообщение:", vigenere.decrypt(text, ALPH, found_key * (len(text) // len(found_key) + 1), 0, False))
