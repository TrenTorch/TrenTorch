def count_in_range(sorted_nums, queries):
    return [sum(1 for v in sorted_nums if lo <= v <= hi) for lo, hi in queries]
