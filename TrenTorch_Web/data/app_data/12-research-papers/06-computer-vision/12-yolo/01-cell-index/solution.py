def cell_index(x, y, img, S):
    col = min(int(x / img * S), S - 1)
    row = min(int(y / img * S), S - 1)
    return (row, col)
