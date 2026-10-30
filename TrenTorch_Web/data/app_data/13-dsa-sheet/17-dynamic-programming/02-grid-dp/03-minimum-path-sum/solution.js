// O(rows * cols) time, O(cols) space
function minPathSum(grid) {
  const rows = grid.length;
  const cols = rows ? grid[0].length : 0;
  if (rows === 0 || cols === 0) {
    return 0;
  }
  const row = new Array(cols).fill(0);
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      if (r === 0 && c === 0) {
        row[c] = grid[0][0];
      } else if (r === 0) {
        row[c] = row[c - 1] + grid[r][c];
      } else if (c === 0) {
        row[c] = row[c] + grid[r][c];
      } else {
        row[c] = Math.min(row[c], row[c - 1]) + grid[r][c];
      }
    }
  }
  return row[cols - 1];
}

console.log(minPathSum([[1, 3, 1], [1, 5, 1], [4, 2, 1]]));
