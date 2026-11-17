def max_points(points, k):
    return max(
        sum(points[:i]) + sum(points[len(points) - (k - i) :] if k - i else [])
        for i in range(k + 1)
    )
