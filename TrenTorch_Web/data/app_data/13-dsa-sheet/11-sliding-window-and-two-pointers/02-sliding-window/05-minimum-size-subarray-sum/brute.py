def min_subarray_len(target, nums):
    best = 0
    for i in range(len(nums)):
        for j in range(i, len(nums)):
            if sum(nums[i : j + 1]) >= target:
                if best == 0 or j - i + 1 < best:
                    best = j - i + 1
                break
    return best
