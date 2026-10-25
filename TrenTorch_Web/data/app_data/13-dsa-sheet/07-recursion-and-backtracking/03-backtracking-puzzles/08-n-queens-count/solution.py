def n_queens_count(n):
    cols, diag1, diag2 = set(), set(), set()

    def go(r):
        if r == n:
            return 1
        total = 0
        for c in range(n):
            if c in cols or r - c in diag1 or r + c in diag2:
                continue
            cols.add(c)
            diag1.add(r - c)
            diag2.add(r + c)
            total += go(r + 1)
            cols.remove(c)
            diag1.remove(r - c)
            diag2.remove(r + c)
        return total

    return go(0)
