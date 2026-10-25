def next_greater(nums):
    out = []
    for i in range(len(nums)):
        out.append(
            next((nums[j] for j in range(i + 1, len(nums)) if nums[j] > nums[i]), -1)
        )
    return out
