def candy(ratings):
    n = len(ratings)
    if n == 0:
        return 0
    total = 1
    up = down = peak = 0
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            up += 1
            down = 0
            peak = up
            total += 1 + up
        elif ratings[i] == ratings[i - 1]:
            up = down = peak = 0
            total += 1
        else:
            up = 0
            down += 1
            total += 1 + down
            if peak >= down:
                total -= 1
    return total
