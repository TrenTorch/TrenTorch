def run_union_find(n, ops):
    parent = list(range(n))
    size = [1] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    out = []
    for op in ops:
        parts = op.split()
        if parts[0] == "union":
            a, b = find(int(parts[1])), find(int(parts[2]))
            if a != b:
                if size[a] < size[b]:
                    a, b = b, a
                parent[b] = a
                size[a] += size[b]
        elif parts[0] == "connected":
            out.append(1 if find(int(parts[1])) == find(int(parts[2])) else 0)
        else:
            out.append(size[find(int(parts[1]))])
    return out
