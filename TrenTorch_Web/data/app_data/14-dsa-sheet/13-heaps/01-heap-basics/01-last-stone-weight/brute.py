def last_stone_weight(stones):
    stones = sorted(stones)
    while len(stones) > 1:
        a = stones.pop()
        b = stones.pop()
        if a != b:
            stones.append(a - b)
            stones.sort()
    return stones[0] if stones else 0
