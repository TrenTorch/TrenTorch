def calculate_minimum_hp(dungeon):
    rows = len(dungeon)
    cols = len(dungeon[0]) if rows else 0
    if rows == 0 or cols == 0:
        return 1
    inf = float("inf")
    need = [inf] * (cols + 1)
    need[cols - 1] = 1
    for r in range(rows - 1, -1, -1):
        for c in range(cols - 1, -1, -1):
            best_next = min(need[c], need[c + 1])
            if r == rows - 1 and c == cols - 1:
                best_next = 1
            need[c] = max(1, best_next - dungeon[r][c])
        need[cols] = inf
    return need[0]
