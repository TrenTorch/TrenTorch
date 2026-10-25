def majority_element_thirds(nums):
    return sorted(v for v in set(nums) if nums.count(v) * 3 > len(nums))
