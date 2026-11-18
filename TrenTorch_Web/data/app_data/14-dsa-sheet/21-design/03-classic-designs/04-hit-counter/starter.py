def run_hit_counter(ops: list[str]) -> list[int]:
    """Run the hit and count operations and return the results of count."""
    # This is correct but too slow: every count looks at all the hits ever recorded.
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
