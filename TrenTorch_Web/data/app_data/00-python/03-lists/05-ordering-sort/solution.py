def sorted_desc_copy(lst: list) -> list:
    return sorted(lst, reverse=True)


def sort_in_place_by_length(words: list) -> None:
    words.sort(key=len)


def last_char(word: str) -> str:
    if word == "":
        return ""
    return word[-1]


def sort_by_last_char(words: list) -> list:
    return sorted(words, key=last_char)


def reversed_copy(lst: list) -> list:
    return list(reversed(lst))
