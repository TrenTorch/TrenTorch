def min_cost_cut(length: int, cuts: list[int]) -> int:
    """Return the least total cost of making all the cuts."""
    # This is correct but too slow: it tries every order of the cuts without remembering results.
    points = [0] + sorted(cuts) + [length]

    def go(i, j):
        if j - i <= 1:
            return 0
        return points[j] - points[i] + min(go(i, k) + go(k, j) for k in range(i + 1, j))

    return go(0, len(points) - 1)
