def connect_ropes(ropes):
    ropes = sorted(ropes)
    total = 0
    while len(ropes) > 1:
        joined = ropes[0] + ropes[1]
        total += joined
        ropes = ropes[2:]
        ropes.append(joined)
        ropes.sort()
    return total
