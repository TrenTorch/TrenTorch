def is_valid_plan(tasks):
    if any(dep not in tasks for deps in tasks.values() for dep in deps):
        return False
    indeg = {t: len(deps) for t, deps in tasks.items()}
    ready = [t for t, d in indeg.items() if d == 0]
    seen = 0
    while ready:
        t = ready.pop()
        seen += 1
        for other, deps in tasks.items():
            if t in deps:
                indeg[other] -= 1
                if indeg[other] == 0:
                    ready.append(other)
    return seen == len(tasks)
