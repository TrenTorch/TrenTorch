def pascal_row(row):
    current = [1]
    for _ in range(row):
        current = (
            [1] + [current[i] + current[i + 1] for i in range(len(current) - 1)] + [1]
        )
    return current
