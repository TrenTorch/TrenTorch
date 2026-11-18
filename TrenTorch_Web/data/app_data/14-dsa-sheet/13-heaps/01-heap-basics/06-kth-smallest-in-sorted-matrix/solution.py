def kth_smallest_matrix(matrix, k):
    rows, cols = len(matrix), len(matrix[0])

    def count_at_most(x):
        count = 0
        col = cols - 1
        for r in range(rows):
            while col >= 0 and matrix[r][col] > x:
                col -= 1
            count += col + 1
        return count

    lo, hi = matrix[0][0], matrix[-1][-1]
    while lo < hi:
        mid = (lo + hi) // 2
        if count_at_most(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo
