def max_water(heights: list[int]) -> int:
    """Return the most water two lines can hold."""
    # This is correct but too slow: it tries every pair of lines.
    best = 0
    for i in range(len(heights)):
        for j in range(i + 1, len(heights)):
            best = max(best, min(heights[i], heights[j]) * (j - i))
    return best
