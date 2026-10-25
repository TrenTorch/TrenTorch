def dice_ways(dice, faces, target):
    if dice == 0:
        return 1 if target == 0 else 0
    return sum(dice_ways(dice - 1, faces, target - f) for f in range(1, faces + 1)) % (
        10**9 + 7
    )
