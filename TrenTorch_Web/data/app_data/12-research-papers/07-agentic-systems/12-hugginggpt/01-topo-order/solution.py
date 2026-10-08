def topo_order(tasks):
    indeg = {t: len(deps) for t, deps in tasks.items()}
    ready = sorted(t for t, d in indeg.items() if d == 0)
    order = []
    while ready:
        t = ready.pop(0)
        order.append(t)
        for other, deps in tasks.items():
            if t in deps:
                indeg[other] -= 1
                if indeg[other] == 0:
                    ready.append(other)
                    ready.sort()
    return order if len(order) == len(tasks) else None
