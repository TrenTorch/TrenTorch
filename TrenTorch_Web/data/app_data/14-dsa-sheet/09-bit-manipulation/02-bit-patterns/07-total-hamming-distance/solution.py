def total_hamming_distance(nums):
    n = len(nums)
    total = 0
    for i in range(30):
        ones = sum((x >> i) & 1 for x in nums)
        total += ones * (n - ones)
    return total
