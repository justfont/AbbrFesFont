import csv


def get_glyph_name(c):
    char_mapping = {
        " ": "space",
        ",": "comma",
        ".": "period",
        "!": "exclam",
        "?": "question",
        ":": "colon",
        "&": "ampersand",
        "(": "parenleft",
        ")": "parenright",
        "'": "quotesingle",
        "、": "comma-han",
        "。": "period-han",
        "，": "comma.full",
        "？": "question.full",
        "！": "exclam.full",
        "～": "asciitilde.full",
        "：": "colon.full",
        "（": "parenleft.full",
        "）": "parenright.full",
        "-": "hyphen",
        "1": "one",
        "2": "two",
        "3": "three",
        "4": "four",
        "5": "five",
        "6": "six",
        "7": "seven",
        "8": "eight",
        "9": "nine",
        "0": "zero",
        "/": "slash",
        "é": "eacute",
        "×": "multiply",
        "+": "plus",
        "ㄊ": "t-bopomofo",
        "ㄟ": "ei-bopomofo",
        "ㄅ": "b-bopomofo",
        "ㄧ": "i-bopomofo",
        "ㄤ": "ang-bopomofo",
        "ˋ": "fourthtonechinese",
    }

    if c in char_mapping:
        return char_mapping[c]
    elif ord(c) >= 0x4E00:
        return f"uni{ord(c):X}"
    return c


def get_glyph_names(source_file, target_file):
    with open(source_file, newline='', encoding='utf-8') as source_file, \
         open(target_file, mode='w', newline='', encoding='utf-8') as target_file:

        reader = csv.reader(source_file)
        writer = csv.writer(target_file)

        seen_first_items = set()

        for row in reader:
            if len(row) < 2:
                continue

            if row[0] in seen_first_items:
                continue

            seen_first_items.add(row[0])
            col1, col2 = row[0], row[1]

            col3 = " ".join(get_glyph_name(c) for c in col1)
            col4 = " ".join(get_glyph_name(c) for c in col2)
            writer.writerow([col1, col2, col3, col4])


def generate_ligatures(glyph_name_file, sub_index, from_words, to_words):
    with open(glyph_name_file, newline='', encoding='utf-8') as glyph_name_file, \
         open(sub_index, mode='w', encoding='utf-8') as sub_index, \
         open(from_words, mode='w', encoding='utf-8') as from_words, \
         open(to_words, mode='w', encoding='utf-8') as to_words:

        reader = csv.reader(glyph_name_file)

        for idx, row in enumerate(reader):
            if len(row) != 4:
                continue

            from_ = row[2].split()
            to_ = row[3].split()

            from_concat = " ".join(from_)
            to_concat = " ".join(to_)

            sub_index.write(f"sub_{idx:04d}\n")
            from_words.write(f"sub {from_concat} by sub_{idx:04d};\n")
            to_words.write(f"sub sub_{idx:04d} by {to_concat};\n")


get_glyph_names('abbrs.csv', 'abbrs_with_glyph_names.csv')
generate_ligatures('abbrs_with_glyph_names.csv', 'sub_index.txt', 'to_ligature.txt', 'from_ligature.txt')
