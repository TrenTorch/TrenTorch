def xor_of_range(left, right):
    def prefix(n):
        if n < 0:
            return 0
        return (n, 1, n + 1, 0)[n % 4]

    return prefix(right) ^ prefix(left - 1)
