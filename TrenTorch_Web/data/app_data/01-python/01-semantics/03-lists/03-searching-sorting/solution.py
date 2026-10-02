def index_or_minus_one(lst: list, value) -> int:
    try:
        return lst.index(value)
    except ValueError:
        return -1


def all_indices(lst: list, value) -> list:
    return [i for i, x in enumerate(lst) if x == value]


def contains_all(lst: list, needles: list) -> bool:
    return all(needle in lst for needle in needles)


def contains_same_object(lst: list, target) -> bool:
    return any(x is target for x in lst)


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
