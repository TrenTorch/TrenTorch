// O(1) time, O(1) space (fixed 9x9 board)
function validSudoku(board) {
  const seen = new Set();
  for (let r = 0; r < 9; r++) {
    for (let c = 0; c < 9; c++) {
      const digit = board[r][c];
      if (digit === 0) continue;
      const box = Math.floor(r / 3) * 3 + Math.floor(c / 3);
      const keys = [
        `row-${r}-${digit}`,
        `col-${c}-${digit}`,
        `box-${box}-${digit}`
      ];
      if (keys.some(key => seen.has(key))) {
        return false;
      }
      keys.forEach(key => seen.add(key));
    }
  }
  return true;
}

console.log(validSudoku([[5, 3, 0, 0, 7, 0, 0, 0, 0], [6, 0, 0, 1, 9, 5, 0, 0, 0], [0, 9, 8, 0, 0, 0, 0, 6, 0], [8, 0, 0, 0, 6, 0, 0, 0, 3], [4, 0, 0, 8, 0, 3, 0, 0, 1], [7, 0, 0, 0, 2, 0, 0, 0, 6], [0, 6, 0, 0, 0, 0, 2, 8, 0], [0, 0, 0, 4, 1, 9, 0, 0, 5], [0, 0, 0, 0, 8, 0, 0, 7, 9]]));
