import re

transitions_table = {
    "ě": "e",
    "š": "s",
    "č": "c",
    "ř": "r",
    "ž": "z",
    "ý": "y",
    "á": "a",
    "í": "i",
    "é": "e",
    "ú": "u",
    "ů": "u",
    "ď": "d",
    "ť": "t",
    "ň": "n",
    "ó": "o",

    "Ě": "E",
    "Š": "S",
    "Č": "C",
    "Ř": "R",
    "Ž": "Z",
    "Ý": "Y",
    "Á": "A",
    "Í": "I",
    "É": "E",
    "Ú": "U",
    "Ů": "U",
    "Ď": "D",
    "Ť": "T",
    "Ň": "N",
    "Ó": "O",
}

preposition_file = open("czech_prepositions.txt", "r", encoding="utf-8")
prepositions = [text.split("\n")[0] for text in preposition_file.readlines()]
preposition_file.close()


def remove_diacritics(word):
    special_chars = transitions_table.keys()
    new_word = []
    for ch in word:
        if ch in special_chars:
            new_char = transitions_table[ch]
            new_word.append(new_char)
        else:
            new_word.append(ch)
    return ''.join(new_word)


def remove_quantity(text):
    next_text = re.sub("[0-9\.,]+(\s\w*)?\s", "", text)
    return next_text


def remove_brackets_with_content(text):
    return re.sub("\(.*\)", "", text)


def text_to_slug(text):
    words = text.split(" ")
    transformed = []
    for word in words:
        transformed.append(word.capitalize())
    return ''.join(transformed)


def remove_prepositions_parts(text):
    words = text.split(' ')
    new_word = []
    for word in words:
        if word in prepositions:
            break
        new_word.append(word)
    return ' '.join(new_word)