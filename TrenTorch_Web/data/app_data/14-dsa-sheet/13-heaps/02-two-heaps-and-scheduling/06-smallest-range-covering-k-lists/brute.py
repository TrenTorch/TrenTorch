def smallest_range(lists):
    best = None
    for lo in sorted({x for lst in lists for x in lst}):
        hi = lo
        ok = True
        for lst in lists:
            candidates = [x for x in lst if x >= lo]
            if not candidates:
                ok = False
                break
            hi = max(hi, min(candidates))
        if ok and (best is None or (hi - lo, lo) < (best[1] - best[0], best[0])):
            best = [lo, hi]
    return best
