from itertools import product


def can_color_graph(n, edges, colors):
    if any(u == v for u, v in edges):
        return False
    return any(
        all(c[u] != c[v] for u, v in edges) for c in product(range(colors), repeat=n)
    )
