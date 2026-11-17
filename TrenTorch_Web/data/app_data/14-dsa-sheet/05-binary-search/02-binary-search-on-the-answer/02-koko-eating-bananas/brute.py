def min_eating_speed(piles, hours):
    for k in range(1, max(piles) + 1):
        if sum(-(-p // k) for p in piles) <= hours:
            return k
