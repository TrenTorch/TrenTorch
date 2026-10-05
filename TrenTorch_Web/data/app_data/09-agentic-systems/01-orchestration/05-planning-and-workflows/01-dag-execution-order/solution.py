def execution_order(tasks):
    for name, deps in tasks.items():
        for d in deps:
            if d not in tasks:
                raise ValueError(f"unknown dependency: {d}")
    remaining = {name: set(deps) for name, deps in tasks.items()}
    order = []
    while remaining:
        ready = sorted(n for n, deps in remaining.items() if not deps)
        if not ready:
            raise ValueError("cycle detected")
        nxt = ready[0]
        order.append(nxt)
        del remaining[nxt]
        for deps in remaining.values():
            deps.discard(nxt)
    return order
