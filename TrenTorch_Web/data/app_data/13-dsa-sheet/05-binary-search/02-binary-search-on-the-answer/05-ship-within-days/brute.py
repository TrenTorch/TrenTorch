def ship_capacity(weights, days):
    for capacity in range(max(weights), sum(weights) + 1):
        needed, load = 1, 0
        for w in weights:
            if load + w > capacity:
                needed += 1
                load = 0
            load += w
        if needed <= days:
            return capacity
