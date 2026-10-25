def median_sliding_window(nums, k):
    out = []
    for i in range(len(nums) - k + 1):
        window = sorted(nums[i : i + k])
        out.append(
            float(window[k // 2])
            if k % 2
            else (window[k // 2 - 1] + window[k // 2]) / 2
        )
    return out
