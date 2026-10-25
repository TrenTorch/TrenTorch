def min_flips(a, b, c):
    best = None
    bits = [(0, i) for i in range(6)] + [(1, i) for i in range(6)]
    for mask in range(1 << 12):
        na, nb = a, b
        for k, (which, i) in enumerate(bits):
            if mask >> k & 1:
                if which == 0:
                    na ^= 1 << i
                else:
                    nb ^= 1 << i
        if na | nb == c and (best is None or bin(mask).count("1") < best):
            best = bin(mask).count("1")
    return best
