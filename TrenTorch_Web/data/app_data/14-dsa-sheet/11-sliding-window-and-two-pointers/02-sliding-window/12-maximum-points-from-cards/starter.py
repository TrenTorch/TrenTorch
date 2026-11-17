def max_points(points: list[int], k: int) -> int:
    """Return the most points from taking k cards from either end."""
    # This is correct but too slow: it tries every split and adds the cards up from scratch.
    return max(
        sum(points[:i]) + sum(points[len(points) - (k - i) :])
        if k - i
        else sum(points[:i])
        for i in range(k + 1)
    )
