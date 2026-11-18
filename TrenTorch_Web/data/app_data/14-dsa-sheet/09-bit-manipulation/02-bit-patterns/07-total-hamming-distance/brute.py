def total_hamming_distance(nums):
    return sum(
        bin(nums[i] ^ nums[j]).count("1")
        for i in range(len(nums))
        for j in range(i + 1, len(nums))
    )
