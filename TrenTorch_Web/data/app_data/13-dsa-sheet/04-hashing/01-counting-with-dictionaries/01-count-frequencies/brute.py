def count_frequencies(nums, queries):
    return [sum(1 for x in nums if x == q) for q in queries]
