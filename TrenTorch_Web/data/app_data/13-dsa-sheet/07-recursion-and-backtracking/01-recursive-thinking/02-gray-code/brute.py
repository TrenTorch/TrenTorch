def gray_code(n):
    codes = [0]
    for bit in range(n):
        codes += [c | (1 << bit) for c in reversed(codes)]
    return codes
