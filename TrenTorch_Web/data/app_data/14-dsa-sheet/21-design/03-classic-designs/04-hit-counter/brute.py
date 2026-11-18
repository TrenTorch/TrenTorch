def run_hit_counter(ops):
    hits = []
    out = []
    for op in ops:
        kind, t = op.split()
        t = int(t)
        if kind == "hit":
            hits.append(t)
        else:
            out.append(sum(1 for h in hits if h > t - 300))
    return out
