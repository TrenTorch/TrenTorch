def minimum_total(triangle):
    if not triangle:
        return 0
    best = triangle[-1][:]
    for row in range(len(triangle) - 2, -1, -1):
        for j in range(row + 1):
            best[j] = triangle[row][j] + min(best[j], best[j + 1])
    return best[0]
