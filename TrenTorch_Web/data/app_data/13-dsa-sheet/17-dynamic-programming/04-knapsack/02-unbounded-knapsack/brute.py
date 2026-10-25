def unbounded_knapsack(weights, values, capacity):
    def go(room):
        best = 0
        for weight, value in zip(weights, values):
            if weight <= room:
                best = max(best, value + go(room - weight))
        return best

    return go(capacity)
