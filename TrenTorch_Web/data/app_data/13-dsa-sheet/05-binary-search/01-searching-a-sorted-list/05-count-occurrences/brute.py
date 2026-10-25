def count_occurrences(nums, target):
    return sum(1 for x in nums if x == target)
