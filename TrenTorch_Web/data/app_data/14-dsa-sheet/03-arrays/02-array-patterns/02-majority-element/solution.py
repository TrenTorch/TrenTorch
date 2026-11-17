def majority_element(nums):
    candidate = None
    count = 0
    for x in nums:
        if count == 0:
            candidate = x
        count += 1 if x == candidate else -1
    if candidate is not None and nums.count(candidate) > len(nums) // 2:
        return candidate
    return -1
