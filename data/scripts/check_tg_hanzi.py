from fontTools.ttLib import TTFont


def load_tg_hanzi():
    with open('tongyong_guifan_hanzi.txt', 'r') as f:
        lines = f.read().splitlines()

    hanzi_set = set()
    for line in lines:
        _, hanzi = line.split()

        hanzi_set.add(hanzi)
    return hanzi_set


def has_glyph(fonts, char):
    for font in fonts:
        for table in font['cmap'].tables:
            if ord(char) in table.cmap.keys():
                return True
    return False


def pretty_print(lst, n_per_row):
    for i in range(0, len(lst), n_per_row):
        block = lst[i:i + n_per_row]
        print("\t".join(block))


def filter_ts_conversions(hanzi_set, fonts):
    """ 刪除不見於 `hanzi_set`，不屬於 Unicode BMP，且未被任何 `fonts` 之一支持的簡化字.
    """
    filename = '../dictionary/TSCharacters.txt'
    with open(filename) as f:
        lines = f.read().splitlines()

    filtered_lines = []
    deleted = []
    retained = []
    for line in lines:
        trad, simp = line.split('\t')
        filtered_simp = []
        for hanzi in simp.split():
            if hanzi not in hanzi_set:
                assert len(hanzi) == 1, f"Not single char: {hanzi}"
                if hanzi <= '\uFFFF' or has_glyph(fonts, hanzi):
                    filtered_simp.append(hanzi)
                    retained.append(f"{hanzi} ({trad})")
                else:
                    deleted.append(f"{hanzi} ({trad})")
            else:
                filtered_simp.append(hanzi)
        if filtered_simp:
            filtered_lines.append(f"{trad}\t{' '.join(filtered_simp)}")

    print(f"保留 {len(retained)} 個不在通用規範漢字表中的簡化字:")
    pretty_print(retained, 15)
    print(f"刪除 {len(deleted)} 個既不在通用規範漢字表中, 也不在基本多文種平面上的簡化字:")
    pretty_print(deleted, 15)

    with open(filename, 'w') as f:
        f.write("\n".join(filtered_lines) + "\n")


if __name__ == '__main__':
    hanzi_set = load_tg_hanzi()
    exceptions = set('鿔鿭𫟷')  # 新元素名稱

    pingfang_sc_regular = TTFont('/System/Library/Fonts/PingFang.ttc', fontNumber=2)

    filter_ts_conversions(hanzi_set | exceptions, [pingfang_sc_regular])
