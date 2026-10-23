def egg_drop(eggs: int, floors: int) -> int:
    """Return the fewest drops that always find the critical floor."""
    # This is correct but too slow: it tries every floor for every sub-problem, with an O(eggs x floors x floors) table.
    best = [[0] * (floors + 1) for _ in range(eggs + 1)]
    for f in range(1, floors + 1):
        best[1][f] = f
    for e in range(2, eggs + 1):
        for f in range(1, floors + 1):
            best[e][f] = 1 + min(
                max(best[e - 1][x - 1], best[e][f - x]) for x in range(1, f + 1)
            )
    return best[eggs][floors] if eggs >= 1 else 0
