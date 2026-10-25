def aggressive_cows(stalls, cows):
    s = sorted(stalls)
    best = 1
    for distance in range(1, s[-1] - s[0] + 1):
        placed, last = 1, s[0]
        for position in s[1:]:
            if position - last >= distance:
                placed += 1
                last = position
        if placed >= cows:
            best = distance
    return best
