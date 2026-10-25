def pascal_row(row):
    out = []
    value = 1
    for i in range(row + 1):
        out.append(value)
        value = value * (row - i) // (i + 1)
    return out
