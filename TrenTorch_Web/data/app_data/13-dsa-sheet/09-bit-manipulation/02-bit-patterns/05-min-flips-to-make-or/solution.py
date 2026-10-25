def min_flips(a, b, c):
    flips = 0
    for i in range(31):
        x, y, z = (a >> i) & 1, (b >> i) & 1, (c >> i) & 1
        if z == 0:
            flips += x + y
        elif x == 0 and y == 0:
            flips += 1
    return flips
