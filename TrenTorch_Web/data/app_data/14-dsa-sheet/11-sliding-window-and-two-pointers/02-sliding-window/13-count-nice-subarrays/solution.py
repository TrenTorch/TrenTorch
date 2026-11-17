def number_of_subarrays(nums, k):
    def at_most(m):
        if m < 0:
            return 0
        odd = 0
        left = 0
        total = 0
        for right, x in enumerate(nums):
            odd += x % 2
            while odd > m:
                odd -= nums[left] % 2
                left += 1
            total += right - left + 1
        return total

    return at_most(k) - at_most(k - 1)
