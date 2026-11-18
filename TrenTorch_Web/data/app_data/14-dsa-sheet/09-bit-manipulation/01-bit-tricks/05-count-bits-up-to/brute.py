def count_bits_up_to(n):
    return [bin(i).count("1") for i in range(n + 1)]
