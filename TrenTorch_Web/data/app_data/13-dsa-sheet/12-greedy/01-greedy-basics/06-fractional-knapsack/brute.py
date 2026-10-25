def fractional_knapsack(items, capacity):
    n = len(items)
    best = 0.0
    for mask in range(1 << n):
        weight = sum(items[i][1] for i in range(n) if mask >> i & 1)
        if weight > capacity:
            continue
        value = float(sum(items[i][0] for i in range(n) if mask >> i & 1))
        best = max(best, value)
        room = capacity - weight
        for j in range(n):
            if not mask >> j & 1:
                best = max(best, value + items[j][0] * min(1.0, room / items[j][1]))
    return best
