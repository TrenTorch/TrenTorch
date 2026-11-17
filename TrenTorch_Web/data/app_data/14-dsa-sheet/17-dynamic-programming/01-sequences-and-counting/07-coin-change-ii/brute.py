def count_change(amount, coins):
    coins = sorted(coins)

    def go(i, rest):
        if rest == 0:
            return 1
        if i == len(coins):
            return 0
        total = 0
        used = 0
        while used * coins[i] <= rest:
            total += go(i + 1, rest - used * coins[i])
            used += 1
        return total

    return go(0, amount) % (10**9 + 7)
