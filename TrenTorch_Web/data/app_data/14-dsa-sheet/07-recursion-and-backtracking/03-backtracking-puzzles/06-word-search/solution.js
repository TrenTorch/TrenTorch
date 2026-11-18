// O(rows * cols * 4^len(word)) time, O(rows * cols + len(word)) space
function wordSearch(board, word) {
  if (!word || word.length === 0) {
    return true;
  }
  const rows = board.length;
  const cols = rows > 0 ? board[0].length : 0;
  const grid = board.map(row => row.split(''));

  function go(r, c, i) {
    if (i === word.length) {
      return true;
    }
    if (r < 0 || r >= rows || c < 0 || c >= cols || grid[r][c] !== word[i]) {
      return false;
    }
    const saved = grid[r][c];
    grid[r][c] = '#';
    const found =
      go(r + 1, c, i + 1) ||
      go(r - 1, c, i + 1) ||
      go(r, c + 1, i + 1) ||
      go(r, c - 1, i + 1);
    grid[r][c] = saved;
    return found;
  }

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      if (go(r, c, 0)) {
        return true;
      }
    }
  }
  return false;
}

console.log(wordSearch(["abce", "sfcs", "adee"], "abcced"));
