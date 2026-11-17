function findWords(board, words) {
  // O(rows * cols * 4^L) time, O(W * L) space (L = max word length, W = total length of words)
  const rows = board.length;
  const cols = rows ? board[0].length : 0;
  // Build trie
  const trie = {};
  for (const word of words) {
    let node = trie;
    for (const ch of word) {
      if (!node[ch]) node[ch] = {};
      node = node[ch];
    }
    node['$'] = word; // mark end of word
  }
  // Convert board to mutable grid
  const grid = board.map(row => row.split(''));
  const found = new Set();

  function dfs(r, c, node) {
    const ch = grid[r][c];
    const next = node[ch];
    if (!next) return;
    if (next['$']) {
      found.add(next['$']);
    }
    grid[r][c] = '#'; // mark visited
    const dirs = [[1,0], [-1,0], [0,1], [0,-1]];
    for (const [dr, dc] of dirs) {
      const nr = r + dr, nc = c + dc;
      if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && grid[nr][nc] !== '#') {
        dfs(nr, nc, next);
      }
    }
    grid[r][c] = ch; // restore
  }

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      dfs(r, c, trie);
    }
  }
  return Array.from(found).sort();
}

console.log(findWords(["oaan", "etae", "ihkr", "iflv"], ["oath", "pea", "eat", "rain"]));
