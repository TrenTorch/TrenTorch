def word_frequencies(text: str) -> dict:
    counts = {}
    for word in text.split():
        counts[word] = counts.get(word, 0) + 1
    return counts


def safe_lookup(d: dict, key, default):
    return d.get(key, default)


def increment(d: dict, key, amount: int) -> None:
    d[key] = d.get(key, 0) + amount


def dict_from_two_lists(keys: list, values: list) -> dict:
    result = {}
    for i in range(len(keys)):
        result[keys[i]] = values[i]
    return result
