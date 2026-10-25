def connect_ropes(ropes: list[int]) -> int:
    """Return the minimum total cost to join all ropes into one."""
    # This is correct but too slow: it sorts the ropes again after every join.
    ropes = sorted(ropes)
    total = 0
    while len(ropes) > 1:
        joined = ropes[0] + ropes[1]
        total += joined
        ropes = ropes[2:]
        ropes.append(joined)
        ropes.sort()
    return total
