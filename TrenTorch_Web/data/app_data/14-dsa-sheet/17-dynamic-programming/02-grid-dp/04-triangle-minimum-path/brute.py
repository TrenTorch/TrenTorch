def minimum_total(triangle):
    if not triangle:
        return 0

    def go(r, j):
        if r == len(triangle) - 1:
            return triangle[r][j]
        return triangle[r][j] + min(go(r + 1, j), go(r + 1, j + 1))

    return go(0, 0)
