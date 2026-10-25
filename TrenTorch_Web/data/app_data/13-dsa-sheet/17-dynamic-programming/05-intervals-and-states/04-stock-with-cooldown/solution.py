def max_profit_cooldown(prices):
    hold = float("-inf")
    sold = rest = 0
    for price in prices:
        hold, sold, rest = max(hold, rest - price), hold + price, max(rest, sold)
    return max(sold, rest)
