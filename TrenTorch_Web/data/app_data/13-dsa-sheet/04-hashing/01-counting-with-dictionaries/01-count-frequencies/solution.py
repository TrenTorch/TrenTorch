from collections import Counter


def count_frequencies(nums, queries):
    counts = Counter(nums)
    return [counts[q] for q in queries]
