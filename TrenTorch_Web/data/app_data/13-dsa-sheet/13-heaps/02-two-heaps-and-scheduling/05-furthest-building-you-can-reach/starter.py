def furthest_building(heights: list[int], bricks: int, ladders: int) -> int:
    """Return the index of the furthest building you can reach."""
    # This is correct but too slow: for every building it sorts all the climbs so far.
    best = 0
    for end in range(1, len(heights)):
        climbs = sorted(
            (
                heights[i] - heights[i - 1]
                for i in range(1, end + 1)
                if heights[i] > heights[i - 1]
            ),
            reverse=True,
        )
        if sum(climbs[ladders:]) <= bricks:
            best = end
        else:
            break
    return best
