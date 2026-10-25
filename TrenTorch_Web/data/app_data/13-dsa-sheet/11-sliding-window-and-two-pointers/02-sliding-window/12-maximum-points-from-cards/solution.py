def max_points(points, k):
    n = len(points)
    size = n - k
    window = sum(points[:size])
    smallest = window
    for i in range(size, n):
        window += points[i] - points[i - size]
        smallest = min(smallest, window)
    return sum(points) - smallest
