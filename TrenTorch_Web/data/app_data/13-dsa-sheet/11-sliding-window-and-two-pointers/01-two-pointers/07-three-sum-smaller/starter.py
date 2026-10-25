def count_triplets_smaller(nums: list[int], target: int) -> int:
    """Count triples of positions i < j < k with nums[i] + nums[j] + nums[k] < target."""
    # This is correct but too slow: it tries every triple.
    count = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            for k in range(j + 1, len(nums)):
                if nums[i] + nums[j] + nums[k] < target:
                    count += 1
    return count
