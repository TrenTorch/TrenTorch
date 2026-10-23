from collections import Counter


def four_sum_count(a, b, c, d):
    sums = Counter(x + y for x in a for y in b)
    return sum(sums[-(z + w)] for z in c for w in d)
