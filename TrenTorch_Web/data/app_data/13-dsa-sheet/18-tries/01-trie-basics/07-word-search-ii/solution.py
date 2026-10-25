def find_words(board, words):
    rows = len(board)
    cols = len(board[0]) if rows else 0
    trie = {}
    for word in words:
        node = trie
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = word
    grid = [list(row) for row in board]
    found = set()

    def dfs(r, c, node):
        ch = grid[r][c]
        nxt = node.get(ch)
        if nxt is None:
            return
        if "$" in nxt:
            found.add(nxt["$"])
        grid[r][c] = "#"
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#":
                dfs(nr, nc, nxt)
        grid[r][c] = ch

    for r in range(rows):
        for c in range(cols):
            dfs(r, c, trie)
    return sorted(found)
