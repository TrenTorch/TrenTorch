def min_refuel_stops(target, start_fuel, stations):
    reach = [start_fuel] + [0] * len(stations)
    for i, (pos, fuel) in enumerate(stations):
        for stops in range(i, -1, -1):
            if reach[stops] >= pos:
                reach[stops + 1] = max(reach[stops + 1], reach[stops] + fuel)
    for stops, far in enumerate(reach):
        if far >= target:
            return stops
    return -1
