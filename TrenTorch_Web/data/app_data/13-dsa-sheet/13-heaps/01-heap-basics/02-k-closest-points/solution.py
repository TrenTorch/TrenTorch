import heapq


def k_closest(points, k):
    return heapq.nsmallest(
        k, points, key=lambda p: (p[0] * p[0] + p[1] * p[1], p[0], p[1])
    )
