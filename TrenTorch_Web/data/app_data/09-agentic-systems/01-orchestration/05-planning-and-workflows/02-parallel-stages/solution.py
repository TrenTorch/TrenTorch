def _memo(tasks, combine):
    cache = {}

    def visit(n):
        if n not in cache:
            cache[n] = combine(n, [visit(d) for d in tasks[n]])
        return cache[n]

    return {n: visit(n) for n in tasks}


def parallel_stages(tasks):
    stage = _memo(tasks, lambda n, ds: 0 if not ds else 1 + max(ds))
    if not stage:
        return []
    out = [[] for _ in range(max(stage.values()) + 1)]
    for n, s in stage.items():
        out[s].append(n)
    return [sorted(s) for s in out]


def critical_path_length(tasks, durations):
    if not tasks:
        return 0.0
    finish = _memo(tasks, lambda n, ds: durations[n] + (max(ds) if ds else 0.0))
    return float(max(finish.values()))
