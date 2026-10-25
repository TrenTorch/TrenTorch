def calculate_minimum_hp(dungeon):
    rows = len(dungeon)
    cols = len(dungeon[0]) if rows else 0
    if rows == 0 or cols == 0:
        return 1
    health = 1
    while True:
        seen = set()

        def survive(r, c, hp):
            hp += dungeon[r][c]
            if hp < 1:
                return False
            if r == rows - 1 and c == cols - 1:
                return True
            if (r, c, hp) in seen:
                return False
            seen.add((r, c, hp))
            return (r + 1 < rows and survive(r + 1, c, hp)) or (
                c + 1 < cols and survive(r, c + 1, hp)
            )

        if survive(0, 0, health):
            return health
        health += 1
