def range_sums(nums, queries):
    return [sum(nums[left : right + 1]) for left, right in queries]
