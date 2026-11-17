def coin_change(coins: list[int], amount: int) -> int:
    """Return the fewest coins that make the amount, or -1."""

    # This is correct but too slow: it solves the same smaller amounts again and again.
    def go(rest):
        if rest == 0:
            return 0
        best = float("inf")
        for c in coins:
            if c <= rest:
                best = min(best, 1 + go(rest - c))
        return best

    answer = go(amount)
    return answer if answer != float("inf") else -1
