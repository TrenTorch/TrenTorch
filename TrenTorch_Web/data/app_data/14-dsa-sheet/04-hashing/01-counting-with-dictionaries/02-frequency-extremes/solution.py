from collections import Counter


def frequency_extremes(nums):
    counts = Counter(nums)
    most = min(counts, key=lambda v: (-counts[v], v))
    least = min(counts, key=lambda v: (counts[v], v))
    return [most, least]
