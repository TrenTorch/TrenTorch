// O(rows * cols) time, O(cols) space
function uniquePathsObstacles(grid) {
  const rows = grid.length;
  const cols = rows ? grid[0].length : 0;
  if (rows === 0 || cols === 0) return 0;
  const mod = 1000000007;
  const row = new Array(cols).fill(0);
  row[0] = grid[0][0] === 0 ? 1 : 0;
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      if (grid[r][c] === 1) {
        row[c] = 0;
      } else if (c > 0) {
        row[c] = (row[c] + row[c - 1]) % mod;
      }
    }
  }
  return row[cols - 1];
}

console.log(uniquePathsObstacles([[0, 0, 0], [0, 1, 0], [0, 0, 0]]));
