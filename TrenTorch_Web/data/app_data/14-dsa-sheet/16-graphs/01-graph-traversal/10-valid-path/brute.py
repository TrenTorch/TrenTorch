def valid_path(n, edges, source, destination):
    reach = {source}
    changed = True
    while changed:
        changed = False
        for a, b in edges:
            if (a in reach) != (b in reach):
                reach.update((a, b))
                changed = True
    return destination in reach
