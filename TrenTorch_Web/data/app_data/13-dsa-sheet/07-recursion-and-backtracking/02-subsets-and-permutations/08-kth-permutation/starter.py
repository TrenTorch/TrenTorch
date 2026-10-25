from itertools import islice, permutations


def kth_permutation(n, k):
    """Return the kth permutation of 1..n in dictionary order, as a string."""
    # This is correct but too slow: it walks through the permutations one by one.
    perm = next(islice(permutations(range(1, n + 1)), k - 1, None))
    return "".join(map(str, perm))
