def is_interleave(a, b, c):
    if len(a) + len(b) != len(c):
        return False

    def go(i, j):
        k = i + j
        if k == len(c):
            return True
        return (i < len(a) and a[i] == c[k] and go(i + 1, j)) or (
            j < len(b) and b[j] == c[k] and go(i, j + 1)
        )

    return go(0, 0)
