def min_platforms(arrivals: list[int], departures: list[int]) -> int:
    """Return the fewest platforms so that no train waits."""
    # This is correct but too slow: for every train it counts the trains in the station.
    best = 0
    for t in arrivals:
        best = max(best, sum(1 for a, d in zip(arrivals, departures) if a <= t <= d))
    return best
