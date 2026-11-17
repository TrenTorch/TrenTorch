def egg_drop(eggs, floors):
    if floors == 0 or eggs == 0:
        return 0
    reach = [0] * (eggs + 1)
    drops = 0
    while reach[eggs] < floors:
        drops += 1
        for e in range(eggs, 0, -1):
            reach[e] = reach[e - 1] + reach[e] + 1
    return drops
