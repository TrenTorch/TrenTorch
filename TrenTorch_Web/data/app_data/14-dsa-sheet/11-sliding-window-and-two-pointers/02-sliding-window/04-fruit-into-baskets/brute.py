def total_fruit(fruits):
    best = 0
    for i in range(len(fruits)):
        for j in range(i, len(fruits)):
            if len(set(fruits[i : j + 1])) <= 2:
                best = max(best, j - i + 1)
    return best
