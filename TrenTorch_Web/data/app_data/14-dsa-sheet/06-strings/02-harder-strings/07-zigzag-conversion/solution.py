def zigzag_conversion(s, rows):
    if rows == 1 or rows >= len(s):
        return s
    lines = [[] for _ in range(rows)]
    row, step = 0, 1
    for ch in s:
        lines[row].append(ch)
        if row == 0:
            step = 1
        elif row == rows - 1:
            step = -1
        row += step
    return "".join("".join(line) for line in lines)
