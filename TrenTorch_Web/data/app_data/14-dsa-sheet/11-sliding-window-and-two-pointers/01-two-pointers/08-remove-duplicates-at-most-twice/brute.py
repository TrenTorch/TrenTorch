from collections import Counter


def keep_at_most_twice(nums):
    seen = Counter()
    out = []
    for x in nums:
        seen[x] += 1
        if seen[x] <= 2:
            out.append(x)
    return out
