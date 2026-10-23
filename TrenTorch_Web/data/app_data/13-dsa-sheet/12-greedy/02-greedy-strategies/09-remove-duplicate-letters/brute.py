from itertools import combinations


def remove_duplicate_letters(s):
    k = len(set(s))
    best = None
    for positions in combinations(range(len(s)), k):
        text = "".join(s[i] for i in positions)
        if len(set(text)) == k and (best is None or text < best):
            best = text
    return best if best is not None else ""
