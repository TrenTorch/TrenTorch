def zigzag_conversion(s, rows):
    if rows == 1:
        return s
    cycle = 2 * (rows - 1)
    out = []
    for r in range(rows):
        for i in range(r, len(s), cycle):
            out.append(s[i])
            other = i + cycle - 2 * r
            if 0 < r < rows - 1 and other < len(s):
                out.append(s[other])
    return "".join(out)
