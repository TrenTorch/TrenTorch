def count_change(amount, coins):
    mod = 10**9 + 7
    ways = [1] + [0] * amount
    for c in coins:
        for a in range(c, amount + 1):
            ways[a] = (ways[a] + ways[a - c]) % mod
    return ways[amount]
