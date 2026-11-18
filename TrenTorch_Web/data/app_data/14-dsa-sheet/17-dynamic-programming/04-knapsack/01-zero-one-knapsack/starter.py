def knapsack(weights: list[int], values: list[int], capacity: int) -> int:
    """Return the largest total value that fits in the bag, using each item at most once."""

    # This is correct but too slow: it tries taking or skipping every item without remembering results.
    def go(i, room):
        if i == len(weights):
            return 0
        best = go(i + 1, room)
        if weights[i] <= room:
            best = max(best, values[i] + go(i + 1, room - weights[i]))
        return best

    return go(0, capacity)
