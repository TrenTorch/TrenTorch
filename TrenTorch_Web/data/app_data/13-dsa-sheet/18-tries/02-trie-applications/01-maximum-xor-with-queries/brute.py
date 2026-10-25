def max_xor_queries(nums, queries):
    return [max(x ^ n for n in nums) for x in queries]
