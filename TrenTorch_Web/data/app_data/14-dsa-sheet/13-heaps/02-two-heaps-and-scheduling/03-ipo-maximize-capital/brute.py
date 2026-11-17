def find_maximized_capital(k, w, profits, capital):
    n = len(profits)

    def go(done, steps, money):
        best = money
        if steps == 0:
            return best
        for i in range(n):
            if not done >> i & 1 and capital[i] <= money:
                best = max(best, go(done | 1 << i, steps - 1, money + profits[i]))
        return best

    return go(0, k, w)
