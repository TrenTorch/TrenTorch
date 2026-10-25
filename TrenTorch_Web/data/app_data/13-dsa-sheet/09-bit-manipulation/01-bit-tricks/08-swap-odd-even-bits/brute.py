def swap_odd_even_bits(n):
    bits = format(n, "032b")[::-1]
    swapped = "".join(bits[i + 1] + bits[i] for i in range(0, 32, 2))
    return int(swapped[::-1], 2)
