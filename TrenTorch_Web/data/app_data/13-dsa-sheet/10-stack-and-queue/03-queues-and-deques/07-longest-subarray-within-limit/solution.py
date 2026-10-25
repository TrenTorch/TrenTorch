from collections import deque


def longest_within_limit(nums, limit):
    big = deque()
    small = deque()
    left = 0
    best = 0
    for right, x in enumerate(nums):
        while big and nums[big[-1]] <= x:
            big.pop()
        big.append(right)
        while small and nums[small[-1]] >= x:
            small.pop()
        small.append(right)
        while nums[big[0]] - nums[small[0]] > limit:
            left += 1
            if big[0] < left:
                big.popleft()
            if small[0] < left:
                small.popleft()
        best = max(best, right - left + 1)
    return best
