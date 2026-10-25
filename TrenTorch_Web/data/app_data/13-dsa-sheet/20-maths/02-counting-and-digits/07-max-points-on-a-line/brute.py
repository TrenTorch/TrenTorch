def max_points(points):
    n = len(points)
    best = min(n, 2)
    for i in range(n):
        for j in range(i + 1, n):
            dx, dy = points[j][0] - points[i][0], points[j][1] - points[i][1]
            count = sum(
                1
                for k in range(n)
                if dx * (points[k][1] - points[i][1])
                == dy * (points[k][0] - points[i][0])
            )
            best = max(best, count)
    return best
