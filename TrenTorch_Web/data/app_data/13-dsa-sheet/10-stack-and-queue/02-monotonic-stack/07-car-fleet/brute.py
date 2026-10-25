from fractions import Fraction


def car_fleet(target, cars):
    times = [Fraction(target - p, s) for p, s in sorted(cars)]
    fleets = 0
    while times:
        fleets += 1
        front = times.pop()
        while times and times[-1] <= front:
            times.pop()
    return fleets
