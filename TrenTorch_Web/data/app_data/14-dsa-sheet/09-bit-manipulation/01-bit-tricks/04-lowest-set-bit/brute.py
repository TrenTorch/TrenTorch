def lowest_set_bit(n):
    bit = 1
    while n and not n & bit:
        bit <<= 1
    return bit if n else 0
