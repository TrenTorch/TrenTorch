from itertools import islice, permutations


def kth_permutation(n, k):
    perm = next(islice(permutations(range(1, n + 1)), k - 1, None))
    return "".join(map(str, perm))
