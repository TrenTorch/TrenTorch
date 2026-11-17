def repeating_and_missing(nums):
    counts = [0] * (len(nums) + 1)
    for x in nums:
        counts[x] += 1
    repeated = counts.index(2)
    missing = counts.index(0, 1)
    return [repeated, missing]
