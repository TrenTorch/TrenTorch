def climb_stairs(n):
    if n <= 1:
        return 1
    return (climb_stairs(n - 1) + climb_stairs(n - 2)) % (10**9 + 7)
