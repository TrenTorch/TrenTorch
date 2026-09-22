def max_pool(matrix: list[list[float]], f: int) -> list[list[float]]:
    n = len(matrix)
    m = n // f
    pooled = []
    for i in range(m):
        pooled_row = []
        for j in range(m):
            # -inf, not 0.0: a patch of all negative values must return its own
            # largest value.
            best = float("-inf")
            for a in range(f):
                row = matrix[i * f + a]
                for b in range(f):
                    value = row[j * f + b]
                    if value > best:
                        best = value
            pooled_row.append(best)
        pooled.append(pooled_row)
    return pooled
