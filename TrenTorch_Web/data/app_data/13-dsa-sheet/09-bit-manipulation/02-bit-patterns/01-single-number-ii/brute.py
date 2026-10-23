from collections import Counter


def single_number_ii(nums):
    return next(v for v, c in Counter(nums).items() if c == 1)
