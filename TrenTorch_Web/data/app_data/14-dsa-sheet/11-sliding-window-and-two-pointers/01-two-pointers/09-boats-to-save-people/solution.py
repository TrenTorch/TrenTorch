def boats_needed(people, limit):
    a = sorted(people)
    light, heavy = 0, len(a) - 1
    boats = 0
    while light <= heavy:
        if a[light] + a[heavy] <= limit:
            light += 1
        heavy -= 1
        boats += 1
    return boats
