def is_power_of_four(n):
    return n > 0 and n & (n - 1) == 0 and n & 0x5555555555555555 != 0
