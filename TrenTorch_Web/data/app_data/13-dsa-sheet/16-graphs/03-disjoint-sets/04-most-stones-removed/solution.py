def remove_stones(stones):
    parent = {}

    def find(a):
        parent.setdefault(a, a)
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for x, y in stones:
        parent[find(x)] = find(y + 10001)
    groups = {find(x) for x, _ in stones}
    return len(stones) - len(groups)
