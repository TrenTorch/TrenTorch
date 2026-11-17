def min_platforms(arrivals, departures):
    best = 0
    for t in arrivals:
        best = max(best, sum(1 for a, d in zip(arrivals, departures) if a <= t <= d))
    return best
