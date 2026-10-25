def min_cost_climbing(cost):
    n = len(cost)

    def go(i):
        if i >= n:
            return 0
        return cost[i] + min(go(i + 1), go(i + 2))

    if n == 0:
        return 0
    return min(go(0), go(1)) if n > 1 else 0
