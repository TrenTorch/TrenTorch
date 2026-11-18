from itertools import accumulate


def range_sums(nums, queries):
    prefix = [0] + list(accumulate(nums))
    return [prefix[right + 1] - prefix[left] for left, right in queries]
