def dice_ways(dice, faces, target):
    mod = 10**9 + 7
    row = [1] + [0] * target
    for _ in range(dice):
        prefix = [0] * (target + 2)
        for t in range(target + 1):
            prefix[t + 1] = (prefix[t] + row[t]) % mod
        nxt = [0] * (target + 1)
        for t in range(1, target + 1):
            nxt[t] = (prefix[t] - prefix[max(0, t - faces)]) % mod
        row = nxt
    return row[target]
