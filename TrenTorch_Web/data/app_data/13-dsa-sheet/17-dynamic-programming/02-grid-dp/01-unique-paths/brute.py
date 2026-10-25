from math import comb


def unique_paths(rows, cols):
    return comb(rows + cols - 2, rows - 1) % (10**9 + 7)
