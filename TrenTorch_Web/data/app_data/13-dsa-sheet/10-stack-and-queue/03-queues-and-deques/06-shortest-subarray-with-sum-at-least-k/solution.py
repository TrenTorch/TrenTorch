from collections import deque


def shortest_subarray_sum_k(nums, k):
    prefix = [0]
    for x in nums:
        prefix.append(prefix[-1] + x)
    best = len(nums) + 1
    window = deque()
    for b, p in enumerate(prefix):
        while window and p - prefix[window[0]] >= k:
            best = min(best, b - window.popleft())
        while window and prefix[window[-1]] >= p:
            window.pop()
        window.append(b)
    return best if best <= len(nums) else -1
