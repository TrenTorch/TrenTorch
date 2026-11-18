def knapsack(weights, values, capacity):
    best = 0
    for mask in range(1 << len(weights)):
        weight = sum(weights[i] for i in range(len(weights)) if mask >> i & 1)
        if weight <= capacity:
            best = max(
                best, sum(values[i] for i in range(len(weights)) if mask >> i & 1)
            )
    return best
