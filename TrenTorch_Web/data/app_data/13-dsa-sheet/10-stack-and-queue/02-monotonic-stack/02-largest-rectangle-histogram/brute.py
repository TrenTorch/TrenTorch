def largest_rectangle(heights):
    best = 0
    for i in range(len(heights)):
        lowest = heights[i]
        for j in range(i, len(heights)):
            lowest = min(lowest, heights[j])
            best = max(best, lowest * (j - i + 1))
    return best
