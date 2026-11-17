def majority_element(nums):
    for x in set(nums):
        if nums.count(x) * 2 > len(nums):
            return x
    return -1
