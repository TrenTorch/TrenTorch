def run_segment_tree(nums, ops):
    n = len(nums)
    inf = float("inf")
    tree = [inf] * n + list(nums)
    for i in range(n - 1, 0, -1):
        tree[i] = min(tree[2 * i], tree[2 * i + 1])
    out = []
    for op in ops:
        parts = op.split()
        if parts[0] == "set":
            i = int(parts[1]) + n
            tree[i] = int(parts[2])
            i //= 2
            while i >= 1:
                tree[i] = min(tree[2 * i], tree[2 * i + 1])
                i //= 2
        else:
            lo, hi = int(parts[1]) + n, int(parts[2]) + n + 1
            best = inf
            while lo < hi:
                if lo & 1:
                    best = min(best, tree[lo])
                    lo += 1
                if hi & 1:
                    hi -= 1
                    best = min(best, tree[hi])
                lo //= 2
                hi //= 2
            out.append(best)
    return out
