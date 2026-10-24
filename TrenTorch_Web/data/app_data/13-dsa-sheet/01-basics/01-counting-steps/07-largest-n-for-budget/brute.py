def largest_n(growth, budget):
    def cost(n):
        if growth == "n":
            return n
        if growth == "n log n":
            return n * (n.bit_length() - 1)
        if growth == "n^2":
            return n * n
        if growth == "n^3":
            return n * n * n
        return 2**n

    best = 0
    n = 1
    while cost(n) <= budget:
        best = n
        n += 1
    return best
