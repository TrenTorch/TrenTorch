from itertools import groupby


def count_and_say(n):
    term = "1"
    for _ in range(n - 1):
        term = "".join(str(len(list(run))) + digit for digit, run in groupby(term))
    return term
