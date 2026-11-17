def assign_cookies(greed, sizes):
    g = sorted(greed)
    child = 0
    for cookie in sorted(sizes):
        if child < len(g) and g[child] <= cookie:
            child += 1
    return child
