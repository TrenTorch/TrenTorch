def median_sliding_window(nums: list[int], k: int) -> list[float]:
    """Return the median of every window of k consecutive values."""
    # This is correct but too slow: it sorts every window from scratch.
    out = []
    for i in range(len(nums) - k + 1):
        window = sorted(nums[i : i + k])
        out.append(
            float(window[k // 2])
            if k % 2
            else (window[k // 2 - 1] + window[k // 2]) / 2
        )
    return out
