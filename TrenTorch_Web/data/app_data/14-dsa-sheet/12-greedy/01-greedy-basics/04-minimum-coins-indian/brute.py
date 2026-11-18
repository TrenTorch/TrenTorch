def fewest_notes(amount):
    values = (1, 2, 5, 10, 20, 50, 100, 500, 2000)
    best = [0] + [float("inf")] * amount
    for a in range(1, amount + 1):
        best[a] = 1 + min(best[a - v] for v in values if v <= a)
    return best[amount]
