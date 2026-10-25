def min_refuel_stops(target: int, start_fuel: int, stations: list[list[int]]) -> int:
    """Return the fewest refuelling stops needed to reach the target, or -1."""
    # This is correct but too slow: it tracks the farthest distance for every possible number of stops.
    reach = [start_fuel] + [0] * len(stations)
    for i, (pos, fuel) in enumerate(stations):
        for stops in range(i, -1, -1):
            if reach[stops] >= pos:
                reach[stops + 1] = max(reach[stops + 1], reach[stops] + fuel)
    for stops, far in enumerate(reach):
        if far >= target:
            return stops
    return -1
