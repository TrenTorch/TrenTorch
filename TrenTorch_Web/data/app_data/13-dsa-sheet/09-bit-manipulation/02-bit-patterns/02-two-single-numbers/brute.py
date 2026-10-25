from collections import Counter


def two_single_numbers(nums):
    return sorted(v for v, c in Counter(nums).items() if c == 1)
