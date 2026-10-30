// O(rows * cols) time, O(cols) space
function minFallingPathSum(matrix) {
  if (!matrix || matrix.length === 0 || matrix[0].length === 0) {
    return 0;
  }
  let prev = [...matrix[0]];
  const cols = prev.length;
  for (let r = 1; r < matrix.length; r++) {
    const curr = new Array(cols);
    for (let c = 0; c < cols; c++) {
      let minPrev = prev[c];
      if (c > 0) minPrev = Math.min(minPrev, prev[c - 1]);
      if (c < cols - 1) minPrev = Math.min(minPrev, prev[c + 1]);
      curr[c] = matrix[r][c] + minPrev;
    }
    prev = curr;
  }
  return Math.min(...prev);
}

console.log(minFallingPathSum([[2, 1, 3], [6, 5, 4], [7, 8, 9]]));
