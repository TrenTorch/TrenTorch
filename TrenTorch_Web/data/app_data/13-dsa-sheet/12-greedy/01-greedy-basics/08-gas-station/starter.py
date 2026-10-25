def gas_station(gas: list[int], cost: list[int]) -> int:
    """Return the smallest starting station that completes the circle, or -1."""
    # This is correct but too slow: it simulates the whole trip from every start.
    n = len(gas)
    for start in range(n):
        tank = 0
        for k in range(n):
            i = (start + k) % n
            tank += gas[i] - cost[i]
            if tank < 0:
                break
        else:
            return start
    return -1
