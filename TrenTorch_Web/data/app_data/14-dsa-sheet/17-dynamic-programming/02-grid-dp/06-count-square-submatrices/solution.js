// O(rows * cols) time, O(cols) space
function countSquares(matrix) {
  const rows = matrix.length;
  const cols = rows > 0 ? matrix[0].length : 0;
  const prev = new Array(cols + 1).fill(0);
  let total = 0;
  for (let r = 0; r < rows; r++) {
    const cur = new Array(cols + 1).fill(0);
    for (let c = 0; c < cols; c++) {
      if (matrix[r][c] === 1) {
        cur[c + 1] = 1 + Math.min(prev[c], prev[c + 1], cur[c]);
        total += cur[c + 1];
      }
    }
    // prev = cur; // In JS, reassigning the variable is fine
    // But we need to update prev reference for next iteration
    // Since we create a new cur each iteration, we can just assign
    prev.length = 0; // clear prev
    prev.push(...cur); // copy cur into prev
    // Alternatively, just reassign: prev = cur; but that would break if prev is used elsewhere? It's local.
    // However, the Python code does `prev = cur` which rebinds the variable.
    // In JS, we can just do `prev = cur` because prev is a let variable.
    // Wait, prev is declared with const. Need to change to let.
  }
  return total;
}

console.log(countSquares([[0, 1, 1, 1], [1, 1, 1, 1], [0, 1, 1, 1]]));
