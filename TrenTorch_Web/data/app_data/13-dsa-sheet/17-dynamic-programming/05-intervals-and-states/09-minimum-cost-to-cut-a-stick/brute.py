from itertools import permutations


def min_cost_cut(length, cuts):
    best = float("inf")
    for order in permutations(cuts):
        pieces = [(0, length)]
        total = 0
        for c in order:
            for idx, (a, b) in enumerate(pieces):
                if a < c < b:
                    total += b - a
                    pieces[idx : idx + 1] = [(a, c), (c, b)]
                    break
        best = min(best, total)
    return best if cuts else 0
