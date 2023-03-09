import math

INPUT_TEXT = """СЪСШ ЩГЖИСЮБЩЫРО ФЧ РЛЫОУУПЦЛЫ ЦЙУБЭЫФСЮДЯ ЛКЧААЮЦЩДХИЯ Б ХЙЕУЖ ШЩ ЧЙХК ЯПУЩА УОРЧЙ ЧЬЩ ЬЙЬЩУЙЙЧ Е ПЛЖЮС ЧАХОИ ЩЦ ЛЩДФСНБЮСЛ Щ ЙККЦЖЦЛЩ ЭЙСНШТ ЩЧЫОВХЮДИ ЗЗН ЛЪЯД ЛЕЖОН ЕЮЧЪЛМСРТЖЦЬВЖ ЛГСЗЙЬЧШ НФЧЗ ЧЮАЮЕ ЛЖЙКУАХЙНАИЕЬВ ЙЦЛ ККФЩУЮИЙЧ З ЬЦСЙВГЫХ СОЗЖЪНШШО ЛЪЯД ЦСЗНКЕШЛГЫХ ЦЩЗШО ЦСПЛЛТП С ЧАХЙВЩ ЮЙЦСЗХФС КЗСАХЦЩ СЙФФЗШО ЛЪЯД РЛЬНГЫХЪЖ ДПХЛЕЗ НФЧГХЛ ШЙ ШУЩ ЮОЕЛХЧУЛУ ЩКЯЙЛЩНКЫЭА ЕЧРЮЗЫГЧЖФЖ ЩЦ ЧРШЙЛЩМ ДЛВОЖЫРО КЙЯЛЫОЖЧЖФПШЙЪНХ ХЙЕЩЖ СЪСШ СЬЛРНГ ШПРТЗПЗН ЧЕЧУЦЖЪЕЩУС РЫСОНШЙ ЩЩТЖЛТЕЗ СЪСПХЛ СПРЬЛЕСЧШЙЪНХЩ ЪЙУЖЫЬЛ ЯЧВАЕЧИ ЩРЩТ ОЕФЖЫХЪЖ ДХЩЩЩХОВХЮДФ ЩРЩТ Щ ЗМУВ ЫЩГЕПЫЛЖПЯЛЩ Е ШУБЭЫЛЯЖ ЛЩДФСНБЮСЖ ШПБВЩ КЛЩА УОРЧЙ С ЛЪЯД Р ЮЯЙЭЩИЙЯЩ ЭЧНЛЯДФ ДЙРЧБЩЫРО ЫФЖ НЖЫФМ ЕРУЛКФТЕЗ У ЬЩУ ЧНШЙЪЖЧКИ ЧЩЫЙЕЧЗАФДЭСФ ЮЙНЭЩСЦТА З СЪСШ РГФПЛТ З ЙЪЬЛЕО ЛР ИОСЩХ АФЧЭЧ ЩЮЯОЧАИОЬШЙО ЦСЙМУБУХЬЛЖ ЪЩНЖЩСБЮСФ НЗНГЯХСЮАКУЛА ЬЙЧБМС Л ГЖФФШПШУБЕФФШЮЧФ ЛЪЬЮАЮСФ НИИ ДЛЯЧЫЛ ЙЩЪБЮСОЛЕЙЬШЙТ СЩЬЦЛ НЖЫФМ Е НФЧКУЩЕ КЙЧК ЮОЩФЦЧЧЩУЧ УБЬЦЩЛЪЩГЖЗО ЛЪЯ ЫГЯ ЭЙЕ ЧЙФПЯЙ ШУЩ ОЫЛР АЪВЛЕСЖР ЪЬЧАХ ЧААКШФЦЖЦГ НЖЫЖЕ ЕЧОЕЙПЬЛКЫП ЩЮЫФСЖЪЬЛТ С РЛЫОУУПЫФТГЦЩМ ЫОЖЧЖФПШЙЪНЩ УЦЩЪЙЧАСПРЛА ХСЦЛЕ ЛЛНЙЛ ЗЛЯХ ЛЪЯ ЦФЩЬКФУЮЧ ЕБЭ ЦФЩЬКФУЮЧ ЯШЙМЩЛЪЩГЖЗО СЩЬЦЛ ЯЙЫЩСАЗ ЩШЗ ЧНСППГЫХ УГЯ ЮОЛЖЪОСШЙ ХЬЛРЧЩФЯЙОЩЖ ЦФДУЧНСД ЦГ ЗЮОЫШЩЗ РРЙПФДХЕ ЛЪЯ ЧЧШЙМЩ ЧЗШГ ЕЙНФТЗ""".replace(" ", "")
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
                if word == "ЩГЖ":
                    print(scan_i, text.find("ЩГЖ"))
                scans[word].add(abs(scan_i - last_i))
                last_i = scan_i

        if len(scans[word]) <= 1:
            scans.pop(word)
    del scanned_words
    print(scans)
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


for search_len in range(2, 64):
    try:
        result = list(scan(INPUT_TEXT.lower(), search_len).items())
        result.sort(key=lambda x: x[1], reverse=True)
        print(result)
        total_count = sum([i[1] for i in result])
        print(f"Возможная длина ключа на повторах длины {search_len}:")
        for e in result[:5]:
            print("Длина", e[0], str(round((e[1] / total_count) * 100)) + "%")
    except KeyError:
        print("Не нашлось повторов длины", search_len)
