// O(rows*cols) time, O(cols) space
function maximalSquare(matrix) {
  const rows = matrix.length;
  const cols = rows ? matrix[0].length : 0;
  let prev = new Array(cols + 1).fill(0);
  let best = 0;
  for (let r = 0; r < rows; r++) {
    const cur = new Array(cols + 1).fill(0);
    for (let c = 0; c < cols; c++) {
      if (matrix[r][c] === 1) {
        cur[c + 1] = 1 + Math.min(prev[c], prev[c + 1], cur[c]);
        if (cur[c + 1] > best) best = cur[c + 1];
      }
    }
    prev = cur;
  }
  return best * best;
}

console.log(maximalSquare([[1, 0, 1, 0, 0], [1, 0, 1, 1, 1], [1, 1, 1, 1, 1], [1, 0, 0, 1, 0]]));
