def max_coins(nums: list[int]) -> int:
    """Return the most coins you can collect by bursting all the balloons."""
    # This is correct but too slow: it tries every order of bursting without remembering results.
    balloons = [1] + nums + [1]

    def go(items):
        if len(items) == 2:
            return 0
        best = 0
        for i in range(1, len(items) - 1):
            gain = items[i - 1] * items[i] * items[i + 1]
            best = max(best, gain + go(items[:i] + items[i + 1 :]))
        return best

    return go(balloons)
