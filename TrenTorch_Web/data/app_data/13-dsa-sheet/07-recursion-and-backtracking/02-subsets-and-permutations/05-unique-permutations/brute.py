from itertools import permutations


def unique_permutations(nums):
    return [list(p) for p in sorted(set(permutations(nums)))]
