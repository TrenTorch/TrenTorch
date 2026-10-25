def dice_ways(dice: int, faces: int, target: int) -> int:
    """Return the number of ways the dice can add up to target, modulo 10**9 + 7."""
    # This is correct but too slow: it tries every face of every die without remembering results.
    if dice == 0:
        return 1 if target == 0 else 0
    return sum(dice_ways(dice - 1, faces, target - f) for f in range(1, faces + 1)) % (
        10**9 + 7
    )
