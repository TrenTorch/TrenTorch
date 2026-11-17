def bit_flips_to_convert(a, b):
    return sum(1 for i in range(40) if (a >> i) & 1 != (b >> i) & 1)
