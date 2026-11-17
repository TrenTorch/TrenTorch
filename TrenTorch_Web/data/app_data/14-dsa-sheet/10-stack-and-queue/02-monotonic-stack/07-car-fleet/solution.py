def car_fleet(target, cars):
    fleets = 0
    slow_num, slow_den = 0, 1
    for pos, spd in sorted(cars, reverse=True):
        num, den = target - pos, spd
        if num * slow_den > slow_num * den:
            fleets += 1
            slow_num, slow_den = num, den
    return fleets
