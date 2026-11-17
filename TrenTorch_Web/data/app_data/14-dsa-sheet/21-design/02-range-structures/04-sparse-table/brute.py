def range_minimums(nums, queries):
    return [min(nums[left : right + 1]) for left, right in queries]
