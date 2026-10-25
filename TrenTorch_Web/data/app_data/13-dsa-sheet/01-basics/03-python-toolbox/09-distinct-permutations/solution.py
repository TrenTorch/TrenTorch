from itertools import permutations


def distinct_permutations(s):
    return sorted({"".join(p) for p in permutations(s)})
