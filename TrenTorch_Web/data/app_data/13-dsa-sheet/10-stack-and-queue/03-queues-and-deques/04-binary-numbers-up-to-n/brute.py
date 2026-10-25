def binary_numbers_up_to(n):
    return [bin(i)[2:] for i in range(1, n + 1)]
