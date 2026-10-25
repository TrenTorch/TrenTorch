def last_stone_weight(stones: list[int]) -> int:
    """Smash the two heaviest stones repeatedly; return the weight of the last stone, or 0."""
    # This is correct but too slow: it sorts all the stones again after every smash.
    stones = sorted(stones)
    while len(stones) > 1:
        a = stones.pop()
        b = stones.pop()
        if a != b:
            stones.append(a - b)
            stones.sort()
    return stones[0] if stones else 0
