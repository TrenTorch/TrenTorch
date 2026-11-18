def remove_stones(stones):
    parent = {}
    size = {}

    def find(a):
        if a not in parent:
            parent[a] = a
            size[a] = 1
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for x, y in stones:
        ra, rb = find(x), find(y + 10001)
        if ra != rb:
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]
    groups = {find(x) for x, _ in stones}
    return len(stones) - len(groups)
