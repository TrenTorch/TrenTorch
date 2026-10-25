from itertools import combinations


def restore_ip_addresses(s):
    out = []
    n = len(s)
    for cuts in combinations(range(1, n), 3):
        bounds = [0, *cuts, n]
        parts = [s[bounds[i] : bounds[i + 1]] for i in range(4)]
        if all((p == "0" or not p.startswith("0")) and int(p) <= 255 for p in parts):
            out.append(".".join(parts))
    return sorted(out)
