from itertools import permutations


def all_permutations(nums):
    return sorted(list(p) for p in permutations(nums))
