def binary_search_index(nums, target):
    for i, x in enumerate(nums):
        if x == target:
            return i
    return -1
