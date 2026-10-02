def squared_unique(values) -> set:
    return {x * x for x in values}


def positive_unique(values) -> set:
    return {x for x in values if x > 0}


def word_lengths(words: list) -> set:
    return {len(word) for word in words}


def coordinate_sums(points: list) -> set:
    return {x + y for x, y in points}
