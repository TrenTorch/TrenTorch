def subarrays_k_distinct(nums, k):
    def at_most(m):
        count = {}
        left = 0
        total = 0
        for right, x in enumerate(nums):
            count[x] = count.get(x, 0) + 1
            while len(count) > m:
                count[nums[left]] -= 1
                if count[nums[left]] == 0:
                    del count[nums[left]]
                left += 1
            total += right - left + 1
        return total

    return at_most(k) - at_most(k - 1)
