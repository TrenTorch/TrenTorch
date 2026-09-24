def first_positions(words: list) -> dict:
    result = {}
    for i, word in enumerate(words):
        if word not in result:
            result[word] = i
    return result


def same_key(a, b) -> bool:
    return hash(a) == hash(b) and a == b


def distinct_key_count(keys: list) -> int:
    d = {}
    for key in keys:
        d[key] = None
    return len(d)
