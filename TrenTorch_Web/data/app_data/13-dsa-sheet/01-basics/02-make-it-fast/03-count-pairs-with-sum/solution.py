from collections import Counter


def count_pairs_with_sum(nums, target):
    seen = Counter()
    count = 0
    for x in nums:
        count += seen[target - x]
        seen[x] += 1
    return count
