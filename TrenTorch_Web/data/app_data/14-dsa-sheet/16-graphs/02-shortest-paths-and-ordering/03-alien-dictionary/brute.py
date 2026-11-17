from itertools import permutations


def alien_order(words):
    letters = sorted({ch for w in words for ch in w})
    for order in permutations(letters):
        rank = {ch: i for i, ch in enumerate(order)}
        ok = True
        for a, b in zip(words, words[1:]):
            key_a = [rank[ch] for ch in a]
            key_b = [rank[ch] for ch in b]
            if key_a > key_b:
                ok = False
                break
        if ok:
            return "".join(order)
    return ""
