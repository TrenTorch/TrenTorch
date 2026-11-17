def ordered_target_encoding(cats, ys, prior, a=1.0):
    sums = {}
    counts = {}
    out = []
    for c, y in zip(cats, ys):
        s = sums.get(c, 0.0)
        n = counts.get(c, 0)
        out.append((s + a * prior) / (n + a))
        sums[c] = s + y
        counts[c] = n + 1
    return out
