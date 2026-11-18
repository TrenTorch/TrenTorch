def search_matrix_ii(matrix, target):
    if not matrix or not matrix[0]:
        return False

    def search(r0, r1, c0, c1):
        # looks for target in rows r0..r1 and columns c0..c1 (both inclusive)
        if r0 > r1 or c0 > c1:
            return False
        if r1 - r0 <= c1 - c0:
            r = (r0 + r1) // 2
            lo, hi = c0, c1 + 1
            while lo < hi:
                mid = (lo + hi) // 2
                if matrix[r][mid] < target:
                    lo = mid + 1
                else:
                    hi = mid
            if lo <= c1 and matrix[r][lo] == target:
                return True
            return search(r0, r - 1, lo, c1) or search(r + 1, r1, c0, lo - 1)
        c = (c0 + c1) // 2
        lo, hi = r0, r1 + 1
        while lo < hi:
            mid = (lo + hi) // 2
            if matrix[mid][c] < target:
                lo = mid + 1
            else:
                hi = mid
        if lo <= r1 and matrix[lo][c] == target:
            return True
        return search(r0, lo - 1, c + 1, c1) or search(lo, r1, c0, c - 1)

    return search(0, len(matrix) - 1, 0, len(matrix[0]) - 1)
