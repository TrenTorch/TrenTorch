def run_fenwick(nums, ops):
    n = len(nums)
    tree = [0] * (n + 1)
    values = list(nums)

    def add(i, delta):
        i += 1
        while i <= n:
            tree[i] += delta
            i += i & -i

    def prefix(i):
        total = 0
        while i > 0:
            total += tree[i]
            i -= i & -i
        return total

    for i, x in enumerate(nums):
        add(i, x)
    out = []
    for op in ops:
        parts = op.split()
        if parts[0] == "set":
            i, v = int(parts[1]), int(parts[2])
            add(i, v - values[i])
            values[i] = v
        else:
            left, right = int(parts[1]), int(parts[2])
            out.append(prefix(right + 1) - prefix(left))
    return out
