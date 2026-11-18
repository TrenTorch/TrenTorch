def next_greater(nums: list[int]) -> list[int]:
    """For each value, return the first greater value to its right, or -1."""
    # This is correct but too slow: it scans to the right from every position.
    out = []
    for i in range(len(nums)):
        answer = -1
        for j in range(i + 1, len(nums)):
            if nums[j] > nums[i]:
                answer = nums[j]
                break
        out.append(answer)
    return out
