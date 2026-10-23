def xor_of_range(left, right):
    result = 0
    for value in range(left, right + 1):
        result ^= value
    return result
