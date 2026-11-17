def max_consecutive_ones(nums):
    text = "".join(str(x) for x in nums)
    return max(len(run) for run in text.split("0"))
