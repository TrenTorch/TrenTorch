def repeating_and_missing(nums):
    n = len(nums)
    diff = sum(nums) - n * (n + 1) // 2
    square_diff = sum(x * x for x in nums) - n * (n + 1) * (2 * n + 1) // 6
    plus = square_diff // diff
    return [(plus + diff) // 2, (plus - diff) // 2]
