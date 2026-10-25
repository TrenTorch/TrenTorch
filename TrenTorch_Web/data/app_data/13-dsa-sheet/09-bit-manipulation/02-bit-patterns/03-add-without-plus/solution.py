def bit_add(a, b):
    mask = 0xFFFFFFFF
    a &= mask
    b &= mask
    while b:
        a, b = (a ^ b) & mask, ((a & b) << 1) & mask
    return a - (1 << 32) if a >= 1 << 31 else a
