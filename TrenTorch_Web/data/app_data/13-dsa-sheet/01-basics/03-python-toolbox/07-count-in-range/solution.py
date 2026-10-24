from bisect import bisect_left, bisect_right


def count_in_range(sorted_nums, queries):
    return [
        bisect_right(sorted_nums, hi) - bisect_left(sorted_nums, lo)
        for lo, hi in queries
    ]
