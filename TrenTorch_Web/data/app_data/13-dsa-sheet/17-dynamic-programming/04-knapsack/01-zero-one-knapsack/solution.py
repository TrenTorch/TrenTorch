def knapsack(weights, values, capacity):
    best = [0] * (capacity + 1)
    for weight, value in zip(weights, values):
        for w in range(capacity, weight - 1, -1):
            if best[w - weight] + value > best[w]:
                best[w] = best[w - weight] + value
    return best[capacity]
