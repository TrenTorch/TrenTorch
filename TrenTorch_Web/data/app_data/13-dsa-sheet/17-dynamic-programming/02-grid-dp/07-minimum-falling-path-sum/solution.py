def min_falling_path_sum(matrix):
    if not matrix or not matrix[0]:
        return 0
    prev = matrix[0][:]
    cols = len(prev)
    for r in range(1, len(matrix)):
        prev = [matrix[r][c] + min(prev[max(0, c - 1) : c + 2]) for c in range(cols)]
    return min(prev)
