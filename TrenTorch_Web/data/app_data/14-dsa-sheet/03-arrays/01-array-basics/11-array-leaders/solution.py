def array_leaders(nums):
    out = []
    best = None
    for x in reversed(nums):
        if best is None or x > best:
            out.append(x)
            best = x
    out.reverse()
    return out
