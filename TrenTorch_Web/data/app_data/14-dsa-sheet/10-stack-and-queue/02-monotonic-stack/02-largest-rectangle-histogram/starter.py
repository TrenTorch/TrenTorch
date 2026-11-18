def largest_rectangle(heights: list[int]) -> int:
    """Return the area of the largest rectangle inside the histogram."""
    # This is correct but too slow: it tries every pair of bars.
    best = 0
    for i in range(len(heights)):
        lowest = heights[i]
        for j in range(i, len(heights)):
            lowest = min(lowest, heights[j])
            best = max(best, lowest * (j - i + 1))
    return best
