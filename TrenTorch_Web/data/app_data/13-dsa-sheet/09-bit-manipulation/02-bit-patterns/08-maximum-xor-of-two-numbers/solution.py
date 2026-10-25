def max_xor_pair(nums):
    best = 0
    for bit in range(29, -1, -1):
        prefixes = {x >> bit for x in nums}
        candidate = (best << 1) | 1
        best <<= 1
        if any((p ^ candidate) in prefixes for p in prefixes):
            best = candidate
    return best
