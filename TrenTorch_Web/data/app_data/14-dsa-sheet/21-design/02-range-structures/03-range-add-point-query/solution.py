def run_range_add(n, ops):
    tree = [0] * (n + 2)

    def add(i, delta):
        i += 1
        while i <= n + 1:
            tree[i] += delta
            i += i & -i

    def prefix(i):
        total = 0
        i += 1
        while i > 0:
            total += tree[i]
            i -= i & -i
        return total

    out = []
    for op in ops:
        parts = op.split()
        if parts[0] == "add":
            left, right, v = int(parts[1]), int(parts[2]), int(parts[3])
            add(left, v)
            add(right + 1, -v)
        else:
            out.append(prefix(int(parts[1])))
    return out
