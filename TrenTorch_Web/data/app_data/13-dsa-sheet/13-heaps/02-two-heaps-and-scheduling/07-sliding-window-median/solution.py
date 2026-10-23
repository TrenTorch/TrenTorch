from bisect import bisect_left, insort


def median_sliding_window(nums, k):
    window = sorted(nums[:k])
    out = []
    for i in range(k, len(nums) + 1):
        if k % 2:
            out.append(float(window[k // 2]))
        else:
            out.append((window[k // 2 - 1] + window[k // 2]) / 2)
        if i == len(nums):
            break
        del window[bisect_left(window, nums[i - k])]
        insort(window, nums[i])
    return out
