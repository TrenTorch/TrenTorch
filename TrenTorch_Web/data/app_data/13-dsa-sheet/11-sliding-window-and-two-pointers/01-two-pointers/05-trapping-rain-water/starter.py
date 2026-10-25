def trap_water(heights: list[int]) -> int:
    """Return how much rain water the bars trap."""
    # This is correct but too slow: it looks for the tallest bar on both sides of every bar.
    total = 0
    for i in range(len(heights)):
        total += min(max(heights[: i + 1]), max(heights[i:])) - heights[i]
    return total
