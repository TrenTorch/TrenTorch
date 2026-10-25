def trap_water(heights):
    total = 0
    for i in range(len(heights)):
        total += min(max(heights[: i + 1]), max(heights[i:])) - heights[i]
    return total
