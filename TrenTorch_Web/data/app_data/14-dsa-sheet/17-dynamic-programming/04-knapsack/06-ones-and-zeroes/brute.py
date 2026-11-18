def find_max_form(strs, m, n):
    best = 0
    for mask in range(1 << len(strs)):
        chosen = [strs[i] for i in range(len(strs)) if mask >> i & 1]
        if (
            sum(s.count("0") for s in chosen) <= m
            and sum(s.count("1") for s in chosen) <= n
        ):
            best = max(best, len(chosen))
    return best
