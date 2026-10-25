def row_with_most_ones(matrix):
    best_row, best = -1, 0
    for i, row in enumerate(matrix):
        lo, hi = 0, len(row)
        while lo < hi:
            mid = (lo + hi) // 2
            if row[mid] == 1:
                hi = mid
            else:
                lo = mid + 1
        ones = len(row) - lo
        if ones > best:
            best_row, best = i, ones
    return best_row
