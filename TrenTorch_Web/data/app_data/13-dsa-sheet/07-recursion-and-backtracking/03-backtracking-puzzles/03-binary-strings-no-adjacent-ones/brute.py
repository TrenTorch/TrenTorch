from itertools import product


def no_adjacent_ones(n):
    return ["".join(p) for p in product("01", repeat=n) if "11" not in "".join(p)]
