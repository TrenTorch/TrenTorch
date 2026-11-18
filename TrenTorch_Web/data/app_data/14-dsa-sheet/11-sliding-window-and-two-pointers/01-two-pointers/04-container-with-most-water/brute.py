def max_water(heights):
    best = 0
    for i in range(len(heights)):
        for j in range(i + 1, len(heights)):
            best = max(best, min(heights[i], heights[j]) * (j - i))
    return best
