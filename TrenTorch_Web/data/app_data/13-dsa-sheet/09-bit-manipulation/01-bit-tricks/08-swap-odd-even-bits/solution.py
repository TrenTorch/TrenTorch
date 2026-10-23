def swap_odd_even_bits(n):
    return ((n & 0x55555555) << 1) | ((n & 0xAAAAAAAA) >> 1)
