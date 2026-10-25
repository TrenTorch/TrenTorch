def find_max_form(strs, m, n):
    best = [[0] * (n + 1) for _ in range(m + 1)]
    for s in strs:
        zeros = s.count("0")
        ones = len(s) - zeros
        for z in range(m, zeros - 1, -1):
            row = best[z]
            source = best[z - zeros]
            for o in range(n, ones - 1, -1):
                if source[o - ones] + 1 > row[o]:
                    row[o] = source[o - ones] + 1
    return best[m][n]
