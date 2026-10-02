def merge_prefer_second(a: dict, b: dict) -> dict:
    result = dict(a)
    result.update(b)
    return result


def merge_counts(a: dict, b: dict) -> dict:
    result = dict(a)
    for key, value in b.items():
        result[key] = result.get(key, 0) + value
    return result


def group_by_first_letter(words: list) -> dict:
    result = {}
    for word in words:
        if word == "":
            continue
        letter = word[0].lower()
        result.setdefault(letter, []).append(word)
    return result


def add_defaults(config: dict, defaults: dict) -> None:
    for key, value in defaults.items():
        config.setdefault(key, value)
