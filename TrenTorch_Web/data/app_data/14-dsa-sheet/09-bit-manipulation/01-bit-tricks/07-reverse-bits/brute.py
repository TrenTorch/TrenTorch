def reverse_bits(n):
    return int(format(n, "032b")[::-1], 2)
