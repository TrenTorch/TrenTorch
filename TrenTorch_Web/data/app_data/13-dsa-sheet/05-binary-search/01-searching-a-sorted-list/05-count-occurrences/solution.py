from bisect import bisect_left, bisect_right


def count_occurrences(nums, target):
    return bisect_right(nums, target) - bisect_left(nums, target)
