def make_connected(n, connections):
    if len(connections) < n - 1:
        return -1
    parent = list(range(n))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    components = n
    for a, b in connections:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            components -= 1
    return components - 1
