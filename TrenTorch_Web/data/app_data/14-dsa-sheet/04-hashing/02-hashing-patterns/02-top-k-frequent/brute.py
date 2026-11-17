def top_k_frequent(nums, k):
    values = sorted(set(nums), key=lambda v: (-nums.count(v), v))
    return values[:k]
