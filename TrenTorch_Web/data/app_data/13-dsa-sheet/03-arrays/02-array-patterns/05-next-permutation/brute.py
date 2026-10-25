from itertools import permutations


def next_permutation(nums):
    ordered = sorted(set(permutations(nums)))
    index = ordered.index(tuple(nums))
    return list(ordered[(index + 1) % len(ordered)])
