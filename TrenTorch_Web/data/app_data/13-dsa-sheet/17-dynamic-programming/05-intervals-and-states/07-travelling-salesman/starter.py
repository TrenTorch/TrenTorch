from itertools import permutations


def tsp(dist: list[list[int]]) -> int:
    """Return the length of the shortest round trip that visits every city once."""
    # This is correct but too slow: it tries every order of the cities.
    n = len(dist)
    if n <= 1:
        return 0
    best = float("inf")
    for order in permutations(range(1, n)):
        total = (
            dist[0][order[0]]
            + sum(dist[order[i]][order[i + 1]] for i in range(n - 2))
            + dist[order[-1]][0]
        )
        best = min(best, total)
    return best
