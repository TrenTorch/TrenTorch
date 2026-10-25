from itertools import permutations


def n_queens_count(n):
    count = 0
    for cols in permutations(range(n)):
        if (
            len({r - c for r, c in enumerate(cols)}) == n
            and len({r + c for r, c in enumerate(cols)}) == n
        ):
            count += 1
    return count
