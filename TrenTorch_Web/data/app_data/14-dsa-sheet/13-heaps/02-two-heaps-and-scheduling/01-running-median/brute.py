def running_median(nums):
    out = []
    for i in range(len(nums)):
        part = sorted(nums[: i + 1])
        m = len(part)
        out.append(
            float(part[m // 2]) if m % 2 else (part[m // 2 - 1] + part[m // 2]) / 2
        )
    return out
