from math import gcd


def max_points(points):
    n = len(points)
    if n <= 2:
        return n
    best = 2
    for i in range(n):
        slopes = {}
        x0, y0 = points[i]
        for j in range(i + 1, n):
            dx, dy = points[j][0] - x0, points[j][1] - y0
            g = gcd(dx, dy)
            dx, dy = dx // g, dy // g
            if dx < 0 or (dx == 0 and dy < 0):
                dx, dy = -dx, -dy
            slopes[(dx, dy)] = slopes.get((dx, dy), 0) + 1
        if slopes:
            best = max(best, max(slopes.values()) + 1)
    return best
