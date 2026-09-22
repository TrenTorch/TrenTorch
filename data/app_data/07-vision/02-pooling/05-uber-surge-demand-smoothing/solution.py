def avg_pool(matrix: list[list[float]], f: int) -> list[list[float]]:
    n = len(matrix)
    m = n // f
    pooled = []
    for i in range(m):
        pooled_row = []
        for j in range(m):
            total = 0.0
            for a in range(f):
                row = matrix[i * f + a]
                for b in range(f):
                    total += row[j * f + b]
            pooled_row.append(total / (f * f))
        pooled.append(pooled_row)
    return pooled
