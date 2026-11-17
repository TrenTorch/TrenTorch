def all_combinations(n, k):
    out = []

    def go(start, current):
        need = k - len(current)
        if need == 0:
            out.append(list(current))
            return
        for j in range(start, n - need + 2):
            current.append(j)
            go(j + 1, current)
            current.pop()

    go(1, [])
    return out
